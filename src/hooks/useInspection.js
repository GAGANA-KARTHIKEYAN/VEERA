/**
 * VEERA — useInspection hook
 *
 * Manages the full inspection workflow state:
 * idle → uploading preview → processing → results/error
 * with multi-round interactive follow-up evidence acquisition.
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import {
  validateImageFile,
  createImagePreview,
  revokeImagePreview,
} from '../utils/imageValidation.js';
import {
  inspectImage,
  inspectFollowUpImage,
  isInMockMode,
  getProcessingStages,
} from '../services/inspectionApi.js';

export const STATES = {
  IDLE: 'idle',
  PREVIEW: 'preview',
  PROCESSING: 'processing',
  RESULTS: 'results',
  ERROR: 'error',
};

export function useInspection() {
  const [state, setState] = useState(STATES.IDLE);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [question, setQuestion] = useState('');
  const [validationError, setValidationError] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [completedStages, setCompletedStages] = useState([]);
  const [activeStage, setActiveStage] = useState(null);
  const [mockScenario, setMockScenario] = useState('defect_detected');
  const [evidenceRounds, setEvidenceRounds] = useState([]); // List of { round, viewType, preview }

  const isSubmitting = useRef(false);

  // Clean up initial preview URL on unmount
  useEffect(() => {
    return () => {
      if (preview?.url) {
        revokeImagePreview(preview.url);
      }
      evidenceRounds.forEach((r) => {
        if (r.preview?.url) revokeImagePreview(r.preview.url);
      });
    };
  }, [preview, evidenceRounds]);

  const selectFile = useCallback(
    async (newFile) => {
      setValidationError(null);
      setError(null);
      setResults(null);
      setEvidenceRounds([]);

      if (preview?.url) {
        revokeImagePreview(preview.url);
        setPreview(null);
      }

      if (!newFile) {
        setFile(null);
        setState(STATES.IDLE);
        return;
      }

      const validation = validateImageFile(newFile);
      if (!validation.valid) {
        setValidationError(validation.error);
        setFile(null);
        setState(STATES.IDLE);
        return;
      }

      try {
        const previewData = await createImagePreview(newFile);
        setFile(newFile);
        setPreview(previewData);
        setState(STATES.PREVIEW);
      } catch (err) {
        setValidationError(err.message);
        setFile(null);
        setState(STATES.IDLE);
      }
    },
    [preview]
  );

  const removeFile = useCallback(() => {
    if (preview?.url) {
      revokeImagePreview(preview.url);
    }
    setFile(null);
    setPreview(null);
    setValidationError(null);
    setError(null);
    setResults(null);
    setEvidenceRounds([]);
    setCompletedStages([]);
    setActiveStage(null);
    setState(STATES.IDLE);
  }, [preview]);

  const submitInspection = useCallback(async () => {
    if (isSubmitting.current) return;

    if (!file) {
      setValidationError('Please select an image to inspect.');
      return;
    }

    const trimmedQuestion = (question || '').trim();
    if (!trimmedQuestion) {
      setValidationError('Please enter a question to guide visual evidence inspection.');
      return;
    }

    isSubmitting.current = true;
    setState(STATES.PROCESSING);
    setError(null);
    setResults(null);
    setValidationError(null);
    setCompletedStages([]);
    setActiveStage('received');

    try {
      const response = await inspectImage(file, {
        question: trimmedQuestion,
        scenario: mockScenario,
        onProgress: (stageId) => {
          setCompletedStages((prev) => (!prev.includes(stageId) ? [...prev, stageId] : prev));
          setActiveStage(stageId);
        },
      });

      setResults(response);
      setEvidenceRounds([
        {
          round: 1,
          viewType: 'initial',
          preview,
          file,
        },
      ]);
      setState(STATES.RESULTS);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during inspection.');
      setState(STATES.ERROR);
    } finally {
      isSubmitting.current = false;
    }
  }, [file, question, mockScenario, preview]);

  /**
   * Submits a follow-up supplemental evidence image for the current inspection.
   */
  const submitFollowUp = useCallback(
    async (followUpFile, viewType = 'close_up') => {
      if (isSubmitting.current || !followUpFile || !results) return;

      const validation = validateImageFile(followUpFile);
      if (!validation.valid) {
        setValidationError(validation.error);
        return;
      }

      isSubmitting.current = true;
      setState(STATES.PROCESSING);
      setError(null);
      setCompletedStages([]);
      setActiveStage('received');

      try {
        const followUpPreview = await createImagePreview(followUpFile);
        const nextRound = (results.round_number || 1) + 1;

        const response = await inspectFollowUpImage(followUpFile, {
          question: results.question || question,
          sessionId: results.session_id,
          roundNumber: nextRound,
          viewType,
          previousHistory: results.evidence_history || [],
          scenario: mockScenario,
          onProgress: (stageId) => {
            setCompletedStages((prev) => (!prev.includes(stageId) ? [...prev, stageId] : prev));
            setActiveStage(stageId);
          },
        });

        setEvidenceRounds((prev) => [
          ...prev,
          {
            round: nextRound,
            viewType,
            preview: followUpPreview,
            file: followUpFile,
          },
        ]);

        setResults(response);
        setState(STATES.RESULTS);
      } catch (err) {
        setError(err.message || 'Error processing supplemental evidence image.');
        setState(STATES.ERROR);
      } finally {
        isSubmitting.current = false;
      }
    },
    [results, question, mockScenario]
  );

  const retryInspection = useCallback(() => {
    if (file && question) {
      submitInspection();
    }
  }, [file, question, submitInspection]);

  const resetInspection = useCallback(() => {
    if (preview?.url) {
      revokeImagePreview(preview.url);
    }
    evidenceRounds.forEach((r) => {
      if (r.preview?.url) revokeImagePreview(r.preview.url);
    });
    setFile(null);
    setPreview(null);
    setQuestion('');
    setValidationError(null);
    setError(null);
    setResults(null);
    setEvidenceRounds([]);
    setCompletedStages([]);
    setActiveStage(null);
    isSubmitting.current = false;
    setState(STATES.IDLE);
  }, [preview, evidenceRounds]);

  return {
    state,
    file,
    preview,
    question,
    validationError,
    results,
    error,
    completedStages,
    activeStage,
    mockScenario,
    evidenceRounds,
    isMockMode: isInMockMode(),
    processingStages: getProcessingStages(),

    selectFile,
    removeFile,
    setQuestion,
    submitInspection,
    submitFollowUp,
    retryInspection,
    resetInspection,
    setMockScenario,
  };
}
