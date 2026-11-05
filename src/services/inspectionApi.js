/**
 * VEERA — Inspection API Service
 *
 * HTTP communication layer for the VEERA Python/FastAPI backend.
 * Conforms to VEERA.pdf structured response contract with support for:
 * - Failure-aware disposition: answered, review, insufficient_evidence
 * - Multi-crop evidence coordinates and thumbnails
 * - Interactive follow-up visual evidence acquisition
 * - Stage-wise latency and device telemetry
 */

import { mockInspect, getMockStages } from '../mocks/inspectionMocks.js';

/**
 * Determine whether mock mode is enabled.
 */
function isMockMode() {
  return import.meta.env.VITE_MOCK_MODE === 'true' || !import.meta.env.VITE_API_BASE_URL;
}

/**
 * Get the base URL for the real backend API.
 */
function getApiBaseUrl() {
  const url = import.meta.env.VITE_API_BASE_URL || '';
  return url.replace(/\/+$/, '');
}

/**
 * Default timeout for inspection requests (ms).
 */
const REQUEST_TIMEOUT_MS = 180_000; // 3 minutes for deep multi-crop VLM passes

/**
 * Validates the backend response shape and normalizes missing optional fields.
 */
function validateAndNormalizeResponse(data, originalQuestion = '') {
  if (!data || typeof data !== 'object') {
    throw new Error('The backend returned an invalid response.');
  }

  if (!data.status) {
    throw new Error('The backend response is missing a status field.');
  }

  // Derive assessment category for styling from status / answer if not explicitly provided
  let assessment = data.assessment;
  if (!assessment) {
    if (data.status === 'review' || data.status === 'insufficient_evidence' || data.answer === 'uncertain') {
      assessment = 'inconclusive';
    } else if (data.answer === 'yes') {
      assessment = 'defect_detected';
    } else if (data.answer === 'no') {
      assessment = 'no_defect';
    } else {
      assessment = 'inconclusive';
    }
  }

  // Normalize optional fields
  return {
    status: data.status, // 'answered' | 'review' | 'insufficient_evidence'
    answer: data.answer || (assessment === 'defect_detected' ? 'yes' : assessment === 'no_defect' ? 'no' : 'uncertain'),
    assessment,
    summary: data.summary || data.reason || (data.status === 'review' ? 'Inconclusive — human review required.' : `Analysis complete: ${data.answer || 'answered'}`),
    reliability_score: typeof data.reliability_score === 'number' ? data.reliability_score : null,
    evidence_inspections: typeof data.evidence_inspections === 'number' ? data.evidence_inspections : (data.verification?.additional_evidence_acquired ? 1 : 0),
    latency_seconds: typeof data.latency_seconds === 'number' ? data.latency_seconds : null,
    reason: data.reason || data.explanation || null,
    crops_inspected: Array.isArray(data.crops_inspected) ? data.crops_inspected : [],
    question: data.question || originalQuestion || null,
    findings: Array.isArray(data.findings) ? data.findings : [],
    verification: data.verification || {
      performed: typeof data.evidence_inspections === 'number' ? data.evidence_inspections > 0 : false,
      additional_evidence_acquired: typeof data.evidence_inspections === 'number' ? data.evidence_inspections > 0 : false,
      initial_assessment: data.reason || null,
      reassessment: null,
    },
    initial_prediction: data.initial_prediction || null,
    initial_gap: typeof data.initial_gap === 'number' ? data.initial_gap : null,
    threshold: typeof data.threshold === 'number' ? data.threshold : 0.7853,
    additional_inspection_performed: !!data.additional_inspection_performed,
    evidence_sufficiency: data.evidence_sufficiency || null,
    requested_evidence: Array.isArray(data.requested_evidence) ? data.requested_evidence : [],
    next_action: data.next_action || null,
    evidence_history: Array.isArray(data.evidence_history) ? data.evidence_history : [],
    session_id: data.session_id || null,
    round_number: typeof data.round_number === 'number' ? data.round_number : 1,
    latency_breakdown: data.latency_breakdown || null,
    device_used: data.device_used || 'cpu',
    explanation: data.explanation || data.reason || null,
    _mock: !!data._mock,
    _mock_scenario: data._mock_scenario || null,
  };
}

/**
 * Inspects an image through the VEERA backend.
 */
export async function inspectImage(file, options = {}) {
  const { question, scenario, onProgress, signal } = options;

  if (isMockMode()) {
    return mockInspect(file, scenario, onProgress, question);
  }

  const baseUrl = getApiBaseUrl();
  if (!baseUrl) {
    throw new Error(
      'No API endpoint configured. Set VITE_API_BASE_URL in your .env file or enable mock mode.'
    );
  }

  const formData = new FormData();
  formData.append('image', file);
  if (question && question.trim()) {
    formData.append('question', question.trim());
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  if (signal) {
    signal.addEventListener('abort', () => controller.abort());
  }

  try {
    if (onProgress) onProgress('received');

    const response = await fetch(`${baseUrl}/api/v1/inspect`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text().catch(() => '');
      if (response.status === 413) {
        throw new Error('The image file is too large for the backend to process.');
      }
      if (response.status === 415) {
        throw new Error('The backend does not support this image format.');
      }
      if (response.status === 422) {
        throw new Error(`Invalid request parameters: ${errorText || 'Ensure image and question are provided.'}`);
      }
      if (response.status === 503) {
        let detailMsg = 'The inspection service is currently unavailable. Please try again later.';
        try {
          const parsed = JSON.parse(errorText);
          if (parsed.detail) detailMsg = parsed.detail;
        } catch {
          if (errorText) detailMsg = errorText;
        }
        throw new Error(detailMsg);
      }
      throw new Error(
        `Inspection failed (HTTP ${response.status}). ${errorText || 'Please try again.'}`
      );
    }

    const data = await response.json();
    return validateAndNormalizeResponse(data, question);
  } catch (err) {
    clearTimeout(timeoutId);

    if (err.name === 'AbortError') {
      throw new Error(
        'The inspection request timed out. Processing multi-crop passes on the VLM may require additional time — please try again.'
      );
    }

    if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
      throw new Error(
        'Unable to connect to the inspection backend. Ensure the FastAPI server / tunnel is running and VITE_API_BASE_URL is correct.'
      );
    }

    throw err;
  }
}

/**
 * Submits supplemental visual evidence requested during an inconclusive inspection.
 */
export async function inspectFollowUpImage(file, options = {}) {
  const {
    question,
    sessionId,
    roundNumber = 2,
    viewType = 'close_up',
    previousHistory = [],
    scenario,
    onProgress,
    signal,
  } = options;

  if (isMockMode()) {
    // In mock mode, simulate resolution or continuation
    const mockRes = await mockInspect(file, scenario || 'defect_detected', onProgress, question);
    mockRes.round_number = roundNumber;
    mockRes.session_id = sessionId || 'mock-session';
    mockRes.evidence_history = [
      ...previousHistory,
      {
        round_number: roundNumber,
        view_type: viewType,
        answer: mockRes.answer,
        reliability_score: mockRes.reliability_score,
        status: mockRes.status,
        reason: `Follow-up (${viewType}) evaluated.`,
      },
    ];
    return mockRes;
  }

  const baseUrl = getApiBaseUrl();
  const formData = new FormData();
  formData.append('image', file);
  formData.append('question', (question || '').trim());
  formData.append('session_id', sessionId || '');
  formData.append('round_number', String(roundNumber));
  formData.append('view_type', viewType);
  if (previousHistory && previousHistory.length > 0) {
    formData.append('previous_history', JSON.stringify(previousHistory));
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  if (signal) signal.addEventListener('abort', () => controller.abort());

  try {
    if (onProgress) onProgress('received');

    const response = await fetch(`${baseUrl}/api/v1/inspect/follow-up`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text().catch(() => '');
      throw new Error(`Follow-up inspection failed (HTTP ${response.status}): ${errorText}`);
    }

    const data = await response.json();
    return validateAndNormalizeResponse(data, question);
  } catch (err) {
    clearTimeout(timeoutId);
    throw err;
  }
}

/**
 * Returns whether the current configuration is in mock mode.
 */
export function isInMockMode() {
  return isMockMode();
}

/**
 * Returns the processing stages (for progress display).
 */
export function getProcessingStages() {
  return getMockStages();
}
