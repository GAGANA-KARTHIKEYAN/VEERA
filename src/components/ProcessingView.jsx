import { CheckCircle, Circle, Loader } from 'lucide-react';

/**
 * VEERA Processing View
 *
 * Displayed while inspection is in progress.
 * Shows image thumbnail, spinner, and progress stages.
 */
export default function ProcessingView({ preview, stages, completedStages, isMockMode }) {
  /**
   * Determine the icon for each stage.
   */
  function getStageIcon(stageId) {
    if (completedStages.includes(stageId)) {
      return <CheckCircle size={18} className="progress-step__icon" aria-hidden="true" />;
    }
    // The next uncompleted stage is "active"
    const nextIndex = completedStages.length;
    const stageIndex = stages.findIndex((s) => s.id === stageId);
    if (stageIndex === nextIndex) {
      return <Loader size={18} className="progress-step__icon" aria-hidden="true" style={{ animation: 'spin 1s linear infinite' }} />;
    }
    return <Circle size={18} className="progress-step__icon" aria-hidden="true" />;
  }

  function getStageClass(stageId) {
    if (completedStages.includes(stageId)) return 'progress-step progress-step--completed';
    const nextIndex = completedStages.length;
    const stageIndex = stages.findIndex((s) => s.id === stageId);
    if (stageIndex === nextIndex) return 'progress-step progress-step--active';
    return 'progress-step';
  }

  return (
    <div className="processing">
      <div className="processing__card" role="status" aria-live="polite">
        {preview?.url && (
          <img
            src={preview.url}
            alt="Image being inspected"
            className="processing__image-thumb"
          />
        )}

        <div className="processing__spinner" aria-hidden="true" />

        <h2 className="processing__title">Inspecting image…</h2>
        <p className="processing__message">
          {isMockMode
            ? 'Running demonstration analysis. This is simulated — not real AI inference.'
            : 'The image is being analyzed. This may take a moment.'}
        </p>

        <div className="progress-steps" aria-label="Processing stages">
          {stages.map((stage) => (
            <div key={stage.id} className={getStageClass(stage.id)}>
              {getStageIcon(stage.id)}
              <span>{stage.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
