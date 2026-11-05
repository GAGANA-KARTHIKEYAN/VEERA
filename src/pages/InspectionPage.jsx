import {
  ScanEye,
  Search,
  Shield,
  Crosshair,
  Lock,
  ArrowRight,
  AlertCircle,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import ImageUpload from '../components/ImageUpload.jsx';
import QuestionInput from '../components/QuestionInput.jsx';
import MockSelector from '../components/MockSelector.jsx';
import ProcessingView from '../components/ProcessingView.jsx';
import InspectionResults from '../components/InspectionResults.jsx';
import ErrorState from '../components/ErrorState.jsx';
import { useInspection, STATES } from '../hooks/useInspection.js';

/**
 * VEERA — Inspection Workspace (Home Page)
 *
 * The primary page. Manages the full workflow:
 * upload → question → preview → inspect → progress → results/error
 */
export default function InspectionPage() {
  const {
    state,
    file,
    preview,
    question,
    validationError,
    results,
    error,
    completedStages,
    mockScenario,
    evidenceRounds,
    isMockMode,
    processingStages,
    selectFile,
    removeFile,
    setQuestion,
    submitInspection,
    submitFollowUp,
    retryInspection,
    resetInspection,
    setMockScenario,
  } = useInspection();

  // --- PROCESSING ---
  if (state === STATES.PROCESSING) {
    return (
      <main className="workspace">
        <div className="container">
          <ProcessingView
            preview={preview}
            stages={processingStages}
            completedStages={completedStages}
            isMockMode={isMockMode}
          />
        </div>
      </main>
    );
  }

  // --- ERROR ---
  if (state === STATES.ERROR) {
    return (
      <main className="workspace">
        <div className="container">
          <ErrorState
            message={error}
            onRetry={file ? retryInspection : null}
            onNewInspection={resetInspection}
          />
        </div>
      </main>
    );
  }

  // --- RESULTS ---
  if (state === STATES.RESULTS && results) {
    return (
      <main className="workspace">
        <div className="container">
          <InspectionResults
            results={results}
            preview={preview}
            evidenceRounds={evidenceRounds}
            isMockMode={isMockMode}
            onNewInspection={resetInspection}
            onRetry={retryInspection}
            onSubmitFollowUp={submitFollowUp}
          />
        </div>
      </main>
    );
  }

  // --- IDLE / PREVIEW ---
  return (
    <main className="workspace">
      <div className="container">
        {/* Header */}
        <div className="workspace__header">
          <h1 className="workspace__title">
            Inspect an image. Find what needs a closer look.
          </h1>
          <p className="workspace__subtitle">
            Upload an image to investigate visible defects and review the evidence behind
            the result.
          </p>
        </div>

        {/* Upload */}
        <ImageUpload
          file={file}
          preview={preview}
          validationError={null}
          onFileSelect={selectFile}
          onRemove={removeFile}
        />

        {/* Natural-Language Question Input */}
        <QuestionInput
          question={question}
          onChange={setQuestion}
          disabled={state === STATES.PROCESSING}
        />

        {/* Validation Error if any */}
        {validationError && (
          <div className="upload-error" role="alert" style={{ marginBottom: 'var(--space-lg)' }}>
            <AlertCircle size={16} className="upload-error__icon" aria-hidden="true" />
            <span>{validationError}</span>
          </div>
        )}

        {/* Mock scenario selector (only shown in mock mode) */}
        {isMockMode && (
          <MockSelector
            selectedScenario={mockScenario}
            onSelectScenario={setMockScenario}
          />
        )}

        {/* Inspect button */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
          <button
            className="btn btn--primary btn--lg"
            onClick={submitInspection}
            type="button"
            id="inspect-button"
            disabled={!file || !question.trim()}
          >
            <ScanEye size={20} aria-hidden="true" />
            Inspect visual evidence
          </button>
          {(!file || !question.trim()) && (
            <p style={{ fontSize: '0.8rem', color: 'var(--color-text-tertiary)', marginTop: 'var(--space-xs)' }}>
              {!file && !question.trim()
                ? 'Select an image and enter a question above to begin inspection.'
                : !file
                ? 'Select an image above to inspect.'
                : 'Enter a question above to guide inspection.'}
            </p>
          )}
        </div>

        {/* Features grid */}
        <div className="features">
          <h2 className="features__title">What VEERA inspects</h2>
          <div className="features__grid">
            <FeatureCard
              icon={<Search size={20} />}
              title="Surface Cracks"
              desc="Identifies potential hairline and structural cracks on surfaces."
            />
            <FeatureCard
              icon={<Crosshair size={20} />}
              title="Damage Detection"
              desc="Examines areas for signs of breakage, chipping, or deformation."
            />
            <FeatureCard
              icon={<Shield size={20} />}
              title="Surface Integrity"
              desc="Evaluates peeling paint, discoloration, or surface irregularities."
            />
          </div>
        </div>

        {/* Methodology link */}
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-xl)' }}>
          <Link to="/about" className="btn btn--ghost">
            Learn about our methodology
            <ArrowRight size={14} aria-hidden="true" />
          </Link>
        </div>

        {/* Privacy note */}
        <div className="privacy-note">
          <Lock size={12} aria-hidden="true" />
          {isMockMode ? (
            <span>
              In mock mode, your image is processed locally in the browser and is not sent
              to any server.
            </span>
          ) : (
            <span>
              Your image is sent to the VEERA backend for analysis. It is not stored
              beyond the inspection session.
            </span>
          )}
        </div>
      </div>
    </main>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="feature-card">
      <div className="feature-card__icon" aria-hidden="true">{icon}</div>
      <h3 className="feature-card__title">{title}</h3>
      <p className="feature-card__desc">{desc}</p>
    </div>
  );
}
