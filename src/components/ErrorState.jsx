import { AlertOctagon, RotateCcw, ArrowLeft } from 'lucide-react';

/**
 * VEERA Error State
 *
 * Displayed when the inspection fails due to network errors,
 * timeouts, backend unavailability, or other issues.
 */
export default function ErrorState({ message, onRetry, onNewInspection }) {
  return (
    <div className="error-state" role="alert">
      <AlertOctagon size={36} className="error-state__icon" aria-hidden="true" />
      <h2 className="error-state__title">Inspection Failed</h2>
      <p className="error-state__message">
        {message || 'An unexpected error occurred. Please try again.'}
      </p>
      <div className="result-actions" style={{ justifyContent: 'center' }}>
        {onRetry && (
          <button className="btn btn--primary" onClick={onRetry} type="button">
            <RotateCcw size={16} aria-hidden="true" />
            Retry
          </button>
        )}
        <button className="btn btn--secondary" onClick={onNewInspection} type="button">
          <ArrowLeft size={16} aria-hidden="true" />
          Start over
        </button>
      </div>
    </div>
  );
}
