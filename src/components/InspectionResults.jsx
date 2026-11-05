import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle,
  HelpCircle,
  Image as ImageIcon,
  Search,
  FileText,
  Eye,
  ShieldAlert,
  Info,
  ArrowLeft,
  RotateCcw,
  Layers,
  Activity,
  Clock,
  Crop,
  UploadCloud,
  Camera,
  Cpu,
  History,
  AlertCircle,
} from 'lucide-react';

/**
 * VEERA Inspection Results Component
 *
 * Implements the Failure-Aware Visual Evidence Acquisition outcome:
 * - Query & failure-aware verdict banner (YES / NO / REVIEW RECOMMENDED)
 * - Explicit abstention alert when visual evidence is insufficient
 * - Empirical reliability metric G(x, q) = |p_Yes - p_No| vs tau = 0.7853
 * - Stage-wise latency breakdown and compute device telemetry
 * - Interactive External Evidence Request (follow-up upload workflow)
 * - Multi-round evidence session timeline
 * - Inspected crops grid with actual thumbnails and coordinates
 * - Side-by-side original image & primary ROI evidence comparison
 */
export default function InspectionResults({
  results,
  preview,
  evidenceRounds = [],
  isMockMode = false,
  onNewInspection,
  onRetry,
  onSubmitFollowUp,
}) {
  if (!results) return null;

  const {
    question,
    status = 'answered',
    answer = 'uncertain',
    reliability_score,
    evidence_inspections = 0,
    latency_seconds,
    reason,
    crops_inspected = [],
    findings = [],
    verification,
    explanation,
    assessment,
    summary,
    initial_prediction,
    initial_gap,
    threshold = 0.7853,
    requested_evidence = [],
    next_action,
    round_number = 1,
    evidence_history = [],
    latency_breakdown,
    device_used = 'cpu',
  } = results;

  const isReview =
    status === 'review' ||
    status === 'insufficient_evidence' ||
    answer === 'uncertain' ||
    assessment === 'inconclusive';

  return (
    <div className="results">
      {/* Mock demonstration banner */}
      {(results._mock || isMockMode) && (
        <div className="results__mock-notice" role="status">
          <Info size={16} aria-hidden="true" />
          <span>
            <strong>Demonstration Mode.</strong> This result is simulated from the test benchmark
            ({results._mock_scenario ? results._mock_scenario.replace('_', ' ') : 'mock data'})
            to illustrate VEERA's failure-aware acquisition architecture.
          </span>
        </div>
      )}

      {/* Query Banner */}
      {question && (
        <div className="results-query-banner">
          <span className="results-query-banner__label">Inspection Query (Round {round_number})</span>
          <h2 className="results-query-banner__text">"{question}"</h2>
        </div>
      )}

      {/* Verdict / Status Banner */}
      <StatusBanner
        status={status}
        answer={answer}
        assessment={assessment}
        summary={summary}
        isReview={isReview}
      />

      {/* Explicit Abstention Notice when human review or further evidence is required */}
      {isReview && (
        <div className="abstention-alert" role="alert">
          <div className="abstention-alert__icon">
            <ShieldAlert size={24} aria-hidden="true" />
          </div>
          <div className="abstention-alert__content">
            <h3 className="abstention-alert__title">
              Failure-Aware Abstention Triggered (Visual Evidence Insufficient)
            </h3>
            <p className="abstention-alert__desc">
              VEERA refused to output an unverified yes/no conclusion because the available visual evidence
              remained contradictory or below the calibrated empirical reliability threshold (&tau; = {(threshold * 100).toFixed(2)}%).
              Under VEERA's failure-awareness policy, ambiguous cases are not guessed; additional evidence must be acquired or verified by human experts.
            </p>
          </div>
        </div>
      )}

      {/* Interactive External Evidence Request (Core Functional Requirement) */}
      {isReview && onSubmitFollowUp && (
        <InteractiveEvidenceRequest
          results={results}
          roundNumber={round_number}
          requestedEvidence={requested_evidence}
          nextAction={next_action}
          onSubmitFollowUp={onSubmitFollowUp}
        />
      )}

      {/* Multi-Round Evidence History Timeline */}
      {(evidence_history.length > 1 || evidenceRounds.length > 1) && (
        <div className="result-section">
          <div className="result-section__header">
            <History size={16} className="result-section__header-icon" aria-hidden="true" />
            Inspection Session History ({evidence_history.length || evidenceRounds.length} Rounds)
          </div>
          <div className="result-section__body">
            <EvidenceHistoryTimeline
              history={evidence_history}
              evidenceRounds={evidenceRounds}
            />
          </div>
        </div>
      )}

      {/* Reliability & Evidence Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-card__header">
            <Activity size={16} className="metric-card__icon" aria-hidden="true" />
            <span>Reliability Signal G(x, q)</span>
          </div>
          <div className="metric-card__value">
            {reliability_score !== null && reliability_score !== undefined
              ? (reliability_score * 100).toFixed(2) + '%'
              : 'N/A'}
          </div>
          <div className="metric-card__subtext">
            Probability gap |p<sub>Yes</sub> - p<sub>No</sub>| (&tau; = {(threshold * 100).toFixed(1)}%)
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card__header">
            <Layers size={16} className="metric-card__icon" aria-hidden="true" />
            <span>Pass Stages</span>
          </div>
          <div className="metric-card__value">
            {initial_prediction ? `Init: ${initial_prediction.toUpperCase()}` : `${evidence_inspections} Crops`}
          </div>
          <div className="metric-card__subtext">
            {initial_gap !== null && initial_gap !== undefined
              ? `Init G(x, q): ${(initial_gap * 100).toFixed(1)}%`
              : `${evidence_inspections} localized crops`}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card__header">
            <Clock size={16} className="metric-card__icon" aria-hidden="true" />
            <span>Total Latency</span>
          </div>
          <div className="metric-card__value">
            {latency_seconds !== undefined && latency_seconds !== null
              ? `${latency_seconds.toFixed(2)}s`
              : 'N/A'}
          </div>
          <div className="metric-card__subtext">
            {latency_breakdown?.initial_inference_seconds !== undefined
              ? `Global: ${latency_breakdown.initial_inference_seconds}s | Crops: ${latency_breakdown.crop_inspection_seconds}s`
              : 'End-to-end visual reasoning time'}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card__header">
            <Cpu size={16} className="metric-card__icon" aria-hidden="true" />
            <span>Compute Device</span>
          </div>
          <div className="metric-card__value" style={{ fontSize: '1.05rem', textTransform: 'uppercase' }}>
            {device_used || 'CPU'}
          </div>
          <div className="metric-card__subtext">
            {device_used?.includes('cuda') ? 'NVIDIA GPU (FP16)' : device_used === 'mps' ? 'Apple Silicon Metal' : 'CPU Fallback'}
          </div>
        </div>
      </div>

      {/* Inspected Crops Section (Multi-crop Visual Evidence) */}
      {crops_inspected && crops_inspected.length > 0 && (
        <div className="result-section">
          <div className="result-section__header">
            <Crop size={16} className="result-section__header-icon" aria-hidden="true" />
            Targeted Visual Crops Inspected ({crops_inspected.length})
          </div>
          <div className="result-section__body">
            <p className="crop-section-desc">
              When initial full-image reliability is insufficient, VEERA allocates compute to inspect targeted
              localized regions to evaluate fine surface details before finalizing a verdict.
            </p>
            <div className="crops-grid">
              {crops_inspected.map((crop, idx) => (
                <div key={crop.id || idx} className="crop-card">
                  <div className="crop-card__header">
                    <span className="crop-card__tag">Crop #{idx + 1}</span>
                    <span className={`crop-vote-badge crop-vote-badge--${crop.vote}`}>
                      Vote: {crop.vote ? crop.vote.toUpperCase() : 'N/A'}
                    </span>
                  </div>
                  {crop.image ? (
                    <div className="crop-card__thumb">
                      <img src={crop.image} alt={crop.label || `Inspected crop ${idx + 1}`} />
                    </div>
                  ) : (
                    <div className="crop-card__placeholder">
                      <span>ROI [{crop.bbox ? crop.bbox.join(', ') : 'Region'}]</span>
                    </div>
                  )}
                  <div className="crop-card__details">
                    <div className="crop-card__label">{crop.label || `Region ${idx + 1}`}</div>
                    {crop.reliability_score !== undefined && (
                      <div className="crop-card__reliability">
                        Local Gap: {(crop.reliability_score * 100).toFixed(2)}%
                      </div>
                    )}
                    {crop.notes && <p className="crop-card__notes">{crop.notes}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Diagnostic Reason / Explanation */}
      {(reason || explanation) && (
        <div className="result-section">
          <div className="result-section__header">
            <FileText size={16} className="result-section__header-icon" aria-hidden="true" />
            Diagnostic Rationale &amp; Reasoning
          </div>
          <div className="result-section__body">
            <p style={{ fontSize: '0.925rem', color: 'var(--color-text-secondary)', lineHeight: 1.7 }}>
              {reason || explanation}
            </p>
          </div>
        </div>
      )}

      {/* Uploaded Image & Evidence Comparison (Fixed Missing Crop Preview) */}
      <div className="result-section">
        <div className="result-section__header">
          <ImageIcon size={16} className="result-section__header-icon" aria-hidden="true" />
          Full Input Image &amp; ROI Evidence
        </div>
        <div className="result-section__body">
          <EvidenceComparison
            preview={preview}
            findings={findings}
            verification={verification}
            crops_inspected={crops_inspected}
          />
        </div>
      </div>

      {/* Detailed Findings List */}
      {findings && findings.length > 0 && (
        <div className="result-section">
          <div className="result-section__header">
            <Search size={16} className="result-section__header-icon" aria-hidden="true" />
            Detailed Findings ({findings.length})
          </div>
          <div className="result-section__body">
            <div className="findings-list">
              {findings.map((finding, idx) => (
                <FindingCard key={idx} finding={finding} />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Verification Pipeline Details */}
      {verification && (
        <div className="result-section">
          <div className="result-section__header">
            <Eye size={16} className="result-section__header-icon" aria-hidden="true" />
            Verification History
          </div>
          <div className="result-section__body">
            <VerificationInfo verification={verification} />
          </div>
        </div>
      )}

      {/* Regulatory & Safety Disclaimer */}
      <div className="result-disclaimer">
        <strong>
          <ShieldAlert size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} aria-hidden="true" />
          Safety Disclaimer:
        </strong>{' '}
        VEERA provides failure-aware visual decision support. All assessments, especially flagged
        abstentions, should be confirmed by certified inspectors before taking irreversible structural
        or maintenance action.
      </div>

      {/* Actions */}
      <div className="result-actions">
        <button className="btn btn--primary" onClick={onNewInspection} type="button">
          <ArrowLeft size={16} aria-hidden="true" />
          Inspect another image
        </button>
        {onRetry && (
          <button className="btn btn--secondary" onClick={onRetry} type="button">
            <RotateCcw size={16} aria-hidden="true" />
            Re-run inspection
          </button>
        )}
      </div>
    </div>
  );
}

/* --------------------------------------------------------
   Interactive Follow-up Evidence Request Component
   -------------------------------------------------------- */

function InteractiveEvidenceRequest({
  _results,
  roundNumber,
  requestedEvidence = [],
  nextAction,
  onSubmitFollowUp,
}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [viewType, setViewType] = useState('close_up');
  const [fileError, setFileError] = useState(null);

  const isMaxReached = nextAction === 'recommend_human_inspection' || roundNumber >= 3;

  const handleFileChange = (e) => {
    const f = e.target.files?.[0];
    if (f) {
      if (f.size > 10 * 1024 * 1024) {
        setFileError('File size exceeds 10 MB limit.');
        setSelectedFile(null);
      } else {
        setFileError(null);
        setSelectedFile(f);
      }
    }
  };

  const handleUploadSubmit = () => {
    if (selectedFile) {
      onSubmitFollowUp(selectedFile, viewType);
    }
  };

  if (isMaxReached) {
    return (
      <div className="followup-evidence-box followup-evidence-box--max-reached">
        <div className="followup-evidence-box__header">
          <AlertCircle size={20} aria-hidden="true" />
          <span>Maximum Iterative Evidence Rounds Reached ({roundNumber}/3)</span>
        </div>
        <p className="followup-evidence-box__desc">
          Automated multi-crop and follow-up evidence analysis could not reach an unambiguous conclusion.
          To prevent catastrophic misclassification, automated evidence collection has stopped.
          <strong> On-site physical inspection by a qualified professional is recommended.</strong>
        </p>
      </div>
    );
  }

  return (
    <div className="followup-evidence-box">
      <div className="followup-evidence-box__header">
        <Camera size={20} aria-hidden="true" />
        <span>Action Required: Requesting Specific Supplemental Visual Evidence</span>
      </div>
      <p className="followup-evidence-box__desc">
        VEERA identified uncertainty in the current image. To resolve this limitation without guessing,
        please upload one of the following requested photographs:
      </p>

      {/* Requested Photograph List */}
      {requestedEvidence && requestedEvidence.length > 0 && (
        <div className="followup-request-list">
          {requestedEvidence.map((req, idx) => (
            <div key={idx} className="followup-request-item">
              <span className="followup-request-item__badge">{req.type.replace('_', ' ')}</span>
              <div>
                <p className="followup-request-item__text"><strong>{req.instruction}</strong></p>
                {req.rationale && (
                  <p style={{ fontSize: '0.75rem', color: '#166534', margin: '2px 0 0 0' }}>
                    {req.rationale}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Supplemental Upload Controls */}
      <div className="followup-upload-zone">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <label style={{ fontSize: '0.75rem', fontWeight: 600, color: '#166534' }}>
            Photographic Viewpoint:
          </label>
          <select
            className="followup-select"
            value={viewType}
            onChange={(e) => setViewType(e.target.value)}
          >
            <option value="close_up">Closer / Macro Detail</option>
            <option value="alternate_angle">Alternate Oblique Angle / Lighting</option>
            <option value="wider_view">Wider Context / Continuation</option>
          </select>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, flex: 1, minWidth: 200 }}>
          <label style={{ fontSize: '0.75rem', fontWeight: 600, color: '#166534' }}>
            Select Follow-up Image:
          </label>
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleFileChange}
            style={{ fontSize: '0.85rem' }}
          />
        </div>

        <button
          className="btn btn--primary"
          style={{ alignSelf: 'flex-end', background: '#16a34a' }}
          onClick={handleUploadSubmit}
          disabled={!selectedFile}
          type="button"
        >
          <UploadCloud size={16} aria-hidden="true" />
          Submit Evidence (Round {roundNumber + 1})
        </button>
      </div>

      {fileError && (
        <p style={{ color: '#b91c1c', fontSize: '0.8rem', marginTop: 8 }}>{fileError}</p>
      )}
    </div>
  );
}

/* --------------------------------------------------------
   Multi-Round History Timeline Component
   -------------------------------------------------------- */

function EvidenceHistoryTimeline({ history = [], evidenceRounds = [] }) {
  const rounds = history.length > 0 ? history : evidenceRounds;

  return (
    <div className="evidence-timeline">
      {rounds.map((item, idx) => {
        const roundNum = item.round_number || item.round || idx + 1;
        const view = item.view_type || item.viewType || 'initial';
        const statusText = item.status || 'review';
        const verdict = item.answer ? item.answer.toUpperCase() : 'UNCERTAIN';
        const thumb = item.preview?.url;

        return (
          <div key={idx} className="evidence-timeline__item">
            <span className="evidence-timeline__round">Round {roundNum}</span>
            {thumb && <img src={thumb} alt={`Round ${roundNum}`} className="evidence-timeline__thumb" />}
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>
                View: {view.replace('_', ' ').toUpperCase()} &bull; Verdict: {verdict}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--color-text-tertiary)' }}>
                Status: {statusText} {item.reliability_score ? `| Gap: ${(item.reliability_score * 100).toFixed(1)}%` : ''}
              </div>
              {item.reason && (
                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', marginTop: 2 }}>
                  {item.reason}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* --------------------------------------------------------
   Sub-components
   -------------------------------------------------------- */

function StatusBanner({ answer, assessment, summary, isReview }) {
  if (isReview) {
    return (
      <div className="status-banner status-banner--inconclusive" role="status">
        <div className="status-banner__icon">
          <HelpCircle size={24} aria-hidden="true" />
        </div>
        <div className="status-banner__content">
          <div className="status-banner__badge status-banner__badge--review">
            REVIEW RECOMMENDED &bull; ABSTENTION
          </div>
          <h2 className="status-banner__title">
            Ambiguous Visual Evidence &mdash; Human Review / Follow-up Advised
          </h2>
          <p className="status-banner__summary">
            {summary || 'Reliability score remained below certainty threshold. The system abstained from a forced decision.'}
          </p>
        </div>
      </div>
    );
  }

  if (answer === 'yes' || assessment === 'defect_detected') {
    return (
      <div className="status-banner status-banner--defect" role="status">
        <div className="status-banner__icon">
          <AlertTriangle size={24} aria-hidden="true" />
        </div>
        <div className="status-banner__content">
          <div className="status-banner__badge status-banner__badge--yes">
            FEATURE DETECTED &bull; YES
          </div>
          <h2 className="status-banner__title">
            Target Feature or Defect Detected
          </h2>
          <p className="status-banner__summary">
            {summary || 'Visual evidence supports the presence of the queried feature or defect.'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="status-banner status-banner--clear" role="status">
      <div className="status-banner__icon">
        <CheckCircle size={24} aria-hidden="true" />
      </div>
      <div className="status-banner__content">
        <div className="status-banner__badge status-banner__badge--no">
          FEATURE NOT DETECTED &bull; NO
        </div>
        <h2 className="status-banner__title">
          No Significant Feature Detected on Inspected Regions
        </h2>
        <p className="status-banner__summary">
          {summary || 'Visual examination revealed no evidence matching the query on inspected surfaces.'}
        </p>
      </div>
    </div>
  );
}

function FindingCard({ finding }) {
  return (
    <div className="finding-card">
      {finding.category && (
        <div className="finding-card__category">{finding.category}</div>
      )}
      {finding.description && (
        <p className="finding-card__description">{finding.description}</p>
      )}
      {finding.evidence && (
        <div className="finding-card__evidence">
          <div className="finding-card__evidence-label">Supporting evidence</div>
          <p>{finding.evidence}</p>
        </div>
      )}
    </div>
  );
}

function EvidenceComparison({ preview, findings, verification, crops_inspected = [] }) {
  // Fix missing crop preview: look for finding.region_image or fall back to primary crop thumbnail
  const regionImage =
    findings?.find((f) => f.region_image)?.region_image ||
    crops_inspected?.[0]?.image;

  const hasAdditionalEvidence =
    verification?.additional_evidence_acquired ||
    (crops_inspected && crops_inspected.length > 0);

  return (
    <div className="evidence-compare">
      <div className="evidence-compare__panel">
        <div className="evidence-compare__label">Original Input Image</div>
        {preview?.url ? (
          <div className="evidence-compare__image">
            <img src={preview.url} alt="Original uploaded image" />
          </div>
        ) : (
          <div className="evidence-compare__placeholder">No image available</div>
        )}
      </div>
      <div className="evidence-compare__panel">
        <div className="evidence-compare__label">Targeted Evidence Region (Primary ROI)</div>
        {regionImage ? (
          <div className="evidence-compare__image">
            <img src={regionImage} alt="Cropped region of interest from the backend" />
          </div>
        ) : (
          <div className="evidence-compare__placeholder">
            {hasAdditionalEvidence
              ? 'Additional evidence was examined, but region image preview is not embedded.'
              : 'Initial full-image assessment was sufficient without supplemental cropping.'}
          </div>
        )}
      </div>
    </div>
  );
}

function VerificationInfo({ verification }) {
  if (!verification) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
      <div className="verification-info">
        <Info size={16} className="verification-info__icon" aria-hidden="true" />
        <span>
          {verification.performed
            ? 'Multi-stage adaptive verification protocol was successfully executed.'
            : 'Single-pass direct verification was sufficient.'}
        </span>
      </div>

      {verification.initial_assessment && (
        <div style={{ padding: 'var(--space-md)', background: 'var(--color-bg-secondary)', borderRadius: 'var(--radius-lg)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.03em', color: 'var(--color-text-tertiary)', marginBottom: 4 }}>
            Initial Global Pass Assessment
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
            {verification.initial_assessment}
          </p>
        </div>
      )}

      {verification.reassessment && (
        <div style={{ padding: 'var(--space-md)', background: 'var(--color-bg-secondary)', borderRadius: 'var(--radius-lg)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.03em', color: 'var(--color-text-tertiary)', marginBottom: 4 }}>
            Crop-Policy Reassessment &amp; Vote
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
            {verification.reassessment}
          </p>
        </div>
      )}
    </div>
  );
}
