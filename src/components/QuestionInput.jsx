import { MessageSquare, Sparkles, X } from 'lucide-react';

const EXAMPLE_QUESTIONS = [
  'Is there a crack on this surface?',
  'Is there a person in this image?',
  'Is there damage on this surface?',
  'Is there peeling paint or corrosion?',
];

/**
 * QuestionInput component for VEERA visual query
 */
export default function QuestionInput({
  question,
  onChange,
  disabled = false,
}) {
  return (
    <div className="question-input-card">
      <div className="question-input-card__header">
        <label htmlFor="inspection-question" className="question-input-card__title">
          <MessageSquare size={18} className="question-input-card__icon" aria-hidden="true" />
          <span>Natural-Language Inspection Query</span>
        </label>
        <span className="question-input-card__badge">Required</span>
      </div>

      <div className="question-input-card__field-wrapper">
        <input
          id="inspection-question"
          type="text"
          className="question-input-card__input"
          placeholder="Ask a question about the image, e.g. 'Is there a crack on this surface?'"
          value={question}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          autoComplete="off"
          aria-label="Inspection query"
        />
        {question && !disabled && (
          <button
            type="button"
            className="question-input-card__clear"
            onClick={() => onChange('')}
            aria-label="Clear question"
          >
            <X size={16} aria-hidden="true" />
          </button>
        )}
      </div>

      <div className="question-input-card__examples">
        <div className="question-input-card__examples-label">
          <Sparkles size={14} aria-hidden="true" />
          <span>Example queries:</span>
        </div>
        <div className="question-input-card__chips">
          {EXAMPLE_QUESTIONS.map((example) => (
            <button
              key={example}
              type="button"
              className={`question-chip ${question === example ? 'question-chip--active' : ''}`}
              onClick={() => onChange(example)}
              disabled={disabled}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

