/**
 * VEERA — Mock inspection responses
 *
 * Provides clearly labelled demonstration data for frontend development.
 * These are NOT real AI outputs. They are mock scenarios for UI testing.
 * Schema adheres to VEERA.pdf (page 13) with full adaptive controller fields.
 */

const _MOCK_DELAY_MS = 3500;

/**
 * Mock processing stages with timing (for progress simulation).
 */
const MOCK_STAGES = [
  { id: 'received', label: 'Image and question received', delay: 400 },
  { id: 'initial', label: 'Initial VLM forward pass', delay: 900 },
  { id: 'sufficiency', label: 'Assessing evidence sufficiency & reliability', delay: 700 },
  { id: 'region', label: 'Targeted visual evidence acquisition (crops)', delay: 900 },
  { id: 'report', label: 'Preparing inspection report & disposition', delay: 500 },
];

/**
 * Scenario: Potential defect detected — a demonstration finding
 * representing a possible crack or requested object, verified by targeted crop.
 */
const MOCK_DEFECT_DETECTED = {
  status: 'answered',
  answer: 'yes',
  assessment: 'defect_detected',
  summary: 'Potential visible surface defect detected (verified by targeted crop inspection).',
  reliability_score: 0.942,
  evidence_inspections: 1,
  latency_seconds: 0.518,
  reason: 'Initial visual evidence identified a potential feature. Targeted crop inspection confirmed the finding.',
  findings: [
    {
      category: 'surface_crack',
      description:
        'A thin, irregular linear feature is visible on the surface, consistent with a potential hairline crack.',
      evidence:
        'The inspected region contains a distinct linear boundary break with high contrast relative to the surrounding texture.',
      region: { x: 0.25, y: 0.35, width: 0.45, height: 0.4 },
      region_image: null,
    },
  ],
  crops_inspected: [
    {
      id: 'crop_1',
      label: 'Region of interest (center-left crop)',
      prediction: 'yes',
      confidence: 0.92,
      note: 'Feature remains clearly visible under higher effective resolution.',
    },
  ],
  verification: {
    performed: true,
    initial_assessment: 'A possible linear irregularity was identified during the initial full-image pass.',
    reassessment:
      'After examining the targeted region, the irregularity remains consistent with a surface defect.',
    additional_evidence_acquired: true,
  },
  explanation:
    'The system identified a potential surface irregularity during initial inspection. A targeted region was examined for additional visual evidence. The feature appears consistent with a crack, though physical inspection by a professional is recommended to confirm structural severity.',
  _mock: true,
  _mock_scenario: 'defect_detected',
};

/**
 * Scenario: No obvious visible defect detected.
 * High initial reliability, no crops needed. Does NOT claim the surface is safe.
 */
const MOCK_NO_DEFECT = {
  status: 'answered',
  answer: 'no',
  assessment: 'no_defect',
  summary: 'No obvious visible defect detected.',
  reliability_score: 0.965,
  evidence_inspections: 0,
  latency_seconds: 0.439,
  reason: 'Initial visual evidence was sufficient (probability gap G >= 0.785). No additional visual evidence required.',
  findings: [],
  crops_inspected: [],
  verification: {
    performed: false,
    initial_assessment:
      'No obvious surface irregularities or target features were identified in the initial visual inspection.',
    reassessment: null,
    additional_evidence_acquired: false,
  },
  explanation:
    'The initial visual inspection did not identify obvious surface defects in the image. The model produced a high reliability score (G = 0.965), so no additional evidence acquisition was triggered, saving inference compute. This result does not guarantee structural integrity — only that no defect was visually apparent to the model.',
  _mock: true,
  _mock_scenario: 'no_defect',
};

/**
 * Scenario: Inconclusive / Abstain / Human Review.
 * Low probability gap, ambiguous crops, stopping policy abstains rather than forcing a wrong answer.
 */
const MOCK_INCONCLUSIVE = {
  status: 'review',
  answer: 'uncertain',
  assessment: 'inconclusive',
  summary: 'Inconclusive — Human review required (model abstained).',
  reliability_score: 0.482,
  evidence_inspections: 4,
  latency_seconds: 1.842,
  reason: 'Initial evidence was uncertain (probability gap G = 0.482). 4-crop inspection yielded contradictory evidence (2 Yes, 2 No). Stopping rule abstains rather than making an unverified guess.',
  findings: [
    {
      category: 'ambiguous_feature',
      description:
        'A possible surface irregularity was detected, but the available visual evidence is insufficient for a confident classification.',
      evidence:
        'The region contains ambiguous shadows and texture variations. Image resolution and lighting limit reliable discernment.',
      region: null,
      region_image: null,
    },
  ],
  crops_inspected: [
    { id: 'crop_top_left', label: 'Crop 1 (Top-Left)', prediction: 'no', note: 'Texture shadow only' },
    { id: 'crop_top_right', label: 'Crop 2 (Top-Right)', prediction: 'yes', note: 'Faint linear feature observed' },
    { id: 'crop_bottom_left', label: 'Crop 3 (Bottom-Left)', prediction: 'no', note: 'No irregularity present' },
    { id: 'crop_bottom_right', label: 'Crop 4 (Bottom-Right)', prediction: 'yes', note: 'Possible surface discoloration' },
  ],
  verification: {
    performed: true,
    initial_assessment:
      'A possible irregularity was detected, but initial confidence was low (probability gap G = 0.482).',
    reassessment:
      'After examining 4 overlapping crops, evidence remains evenly split (2 votes Yes, 2 votes No). The system stopped and abstained.',
    additional_evidence_acquired: true,
  },
  explanation:
    'The system identified a possible feature but could not reach a confident assessment. The adaptive controller acquired 4 overlapping crops, but visual evidence remained contradictory. In accordance with VEERA research guidelines, the system refuses to force a prediction and requests human inspection.',
  _mock: true,
  _mock_scenario: 'inconclusive',
};

/**
 * Map of available mock scenarios.
 */
export const MOCK_SCENARIOS = {
  defect_detected: {
    label: 'Defect detected (Verified Yes)',
    description: 'Simulates a verified finding with 1 targeted crop inspection',
    response: MOCK_DEFECT_DETECTED,
  },
  no_defect: {
    label: 'No defect (Confident No)',
    description: 'Simulates a confident negative result (0 crops acquired, compute saved)',
    response: MOCK_NO_DEFECT,
  },
  inconclusive: {
    label: 'Inconclusive (Abstain / Review)',
    description: 'Simulates low confidence and mixed crop evidence (4 crops, system abstains)',
    response: MOCK_INCONCLUSIVE,
  },
};

/**
 * Returns mock processing stages for progress simulation.
 */
export function getMockStages() {
  return MOCK_STAGES;
}

/**
 * Simulates the inspection API call with progress callbacks.
 *
 * @param {File} file - The uploaded image file.
 * @param {string} scenario - One of 'defect_detected', 'no_defect', 'inconclusive'.
 * @param {function} onProgress - Callback receiving (stageId) as each stage completes.
 * @param {string} [question] - Optional user question for display in mock output.
 * @returns {Promise<object>} The mock inspection response.
 */
export function mockInspect(file, scenario = 'defect_detected', onProgress, question = '') {
  const baseMock = MOCK_SCENARIOS[scenario]?.response || MOCK_DEFECT_DETECTED;
  const mockResponse = {
    ...baseMock,
    question: question || 'Is there a crack on this surface?',
  };

  return new Promise((resolve) => {
    const stages = [...MOCK_STAGES];

    // If scenario is no_defect, skip the "region" stage
    const filteredStages =
      scenario === 'no_defect'
        ? stages.filter((s) => s.id !== 'region')
        : stages;

    function runStage(index) {
      if (index >= filteredStages.length) {
        resolve({ ...mockResponse });
        return;
      }

      const stage = filteredStages[index];
      setTimeout(() => {
        if (onProgress) {
          onProgress(stage.id);
        }
        runStage(index + 1);
      }, stage.delay);
    }

    runStage(0);
  });
}

