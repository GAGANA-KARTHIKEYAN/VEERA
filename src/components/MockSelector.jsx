import { FlaskConical } from 'lucide-react';
import { MOCK_SCENARIOS } from '../mocks/inspectionMocks.js';

/**
 * VEERA Mock Scenario Selector
 *
 * Development-only component that lets the developer choose
 * which mock scenario to use. Clearly labelled as demonstration/development.
 */
export default function MockSelector({ selectedScenario, onSelectScenario }) {
  return (
    <div className="mock-selector" role="group" aria-label="Mock scenario selector (development only)">
      <div className="mock-selector__title">
        <FlaskConical size={14} aria-hidden="true" />
        Demo Scenario (Development Only)
      </div>
      <div className="mock-selector__options">
        {Object.entries(MOCK_SCENARIOS).map(([key, scenario]) => (
          <button
            key={key}
            className={`mock-selector__option ${
              selectedScenario === key ? 'mock-selector__option--active' : ''
            }`}
            onClick={() => onSelectScenario(key)}
            type="button"
            aria-pressed={selectedScenario === key}
            title={scenario.description}
          >
            {scenario.label}
          </button>
        ))}
      </div>
    </div>
  );
}
