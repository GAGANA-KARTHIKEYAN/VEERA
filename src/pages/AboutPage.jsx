import {
  BookOpen,
  Eye,
  Brain,
  HelpCircle,
  Crop,
  Scale,
  ChevronRight,
  ScanEye,
  AlertTriangle,
} from 'lucide-react';

/**
 * VEERA — About / Methodology Page
 *
 * Explains VEERA's research objective, pipeline, and limitations.
 */
export default function AboutPage() {
  return (
    <main className="about-page">
      <div className="container">
        <h1 className="about-page__title">Methodology</h1>
        <p className="about-page__subtitle">
          How VEERA investigates visible defects and acquires evidence for reliable
          visual inspection.
        </p>

        {/* Research Objective */}
        <section className="about-section">
          <h2 className="about-section__title">
            <BookOpen size={18} className="about-section__title-icon" aria-hidden="true" />
            Research Objective
          </h2>
          <p>
            VEERA — <em>Failure-Aware Visual Evidence Acquisition for Reliable Multimodal AI</em> —
            is a research prototype that investigates how vision-language models can
            perform visual inspection tasks while remaining aware of their own limitations.
          </p>
          <p>
            Rather than producing a single pass/fail classification, VEERA explores a
            workflow in which additional visual evidence is acquired when the initial
            assessment is uncertain, and an inconclusive result is reported when the
            available evidence is insufficient.
          </p>
        </section>

        {/* Vision-Language Model */}
        <section className="about-section">
          <h2 className="about-section__title">
            <Brain size={18} className="about-section__title-icon" aria-hidden="true" />
            The Vision-Language Model
          </h2>
          <p>
            VEERA uses <strong>Qwen2.5-VL-3B-Instruct</strong>, a multimodal AI model
            capable of understanding both images and text. The model examines uploaded
            images and generates descriptions of what it observes, including potential
            surface irregularities.
          </p>
          <p>
            The model processes the image and generates a natural-language description.
            This description is then structured by the VEERA pipeline to produce an
            assessment with supporting evidence.
          </p>
        </section>

        {/* Why Uncertainty Matters */}
        <section className="about-section">
          <h2 className="about-section__title">
            <HelpCircle size={18} className="about-section__title-icon" aria-hidden="true" />
            Why Uncertainty Matters
          </h2>
          <p>
            In visual inspection, overconfident assessments can be dangerous. A model
            that reports "no defect" when it cannot actually determine the condition of
            a surface creates a false sense of security.
          </p>
          <p>
            VEERA is designed to distinguish between:
          </p>
          <ul>
            <li>
              <strong>Confident findings:</strong> clear visual evidence supports the assessment.
            </li>
            <li>
              <strong>Uncertain observations:</strong> something may be present, but the evidence
              is ambiguous.
            </li>
            <li>
              <strong>Inconclusive results:</strong> the available image does not provide enough
              information for a reliable assessment.
            </li>
          </ul>
        </section>

        {/* Targeted Evidence Acquisition */}
        <section className="about-section">
          <h2 className="about-section__title">
            <Crop size={18} className="about-section__title-icon" aria-hidden="true" />
            Targeted Evidence Acquisition
          </h2>
          <p>
            When the initial inspection identifies a region of interest but the evidence
            is insufficient, VEERA can examine a targeted crop of the original image
            for additional detail. This simulates a "closer look" at a specific area.
          </p>
          <p>
            The system decides whether additional evidence is needed based on the
            initial assessment's confidence. If the model is already confident, no
            additional crop is examined — saving computation and avoiding unnecessary
            verification steps.
          </p>
        </section>

        {/* Cost-Accuracy Balance */}
        <section className="about-section">
          <h2 className="about-section__title">
            <Scale size={18} className="about-section__title-icon" aria-hidden="true" />
            Balancing Correctness, Cost, and Latency
          </h2>
          <p>
            Each additional evidence-acquisition step adds inference time and computation
            cost. VEERA explores the trade-off between:
          </p>
          <ul>
            <li>
              <strong>Correctness:</strong> more evidence may improve accuracy.
            </li>
            <li>
              <strong>Cost:</strong> each model call consumes GPU resources.
            </li>
            <li>
              <strong>Latency:</strong> users expect timely results.
            </li>
          </ul>
          <p>
            An appropriate stopping criterion prevents unnecessary verification while
            ensuring that ambiguous cases receive additional examination.
          </p>
        </section>

        {/* Pipeline */}
        <section className="about-section">
          <h2 className="about-section__title">
            <ScanEye size={18} className="about-section__title-icon" aria-hidden="true" />
            Inspection Pipeline
          </h2>
          <div className="pipeline" role="img" aria-label="VEERA inspection pipeline: Image, Initial assessment, Evidence sufficiency check, Targeted evidence acquisition when needed, Reassessment, Final result">
            <PipelineStep icon={<Eye size={14} />} label="Image" />
            <PipelineArrow />
            <PipelineStep icon={<ScanEye size={14} />} label="Initial Assessment" />
            <PipelineArrow />
            <PipelineStep icon={<HelpCircle size={14} />} label="Evidence Sufficiency" />
            <PipelineArrow />
            <PipelineStep icon={<Crop size={14} />} label="Targeted Acquisition" />
            <PipelineArrow />
            <PipelineStep icon={<Brain size={14} />} label="Reassessment" />
            <PipelineArrow />
            <PipelineStep icon={<AlertTriangle size={14} />} label="Final Result" />
          </div>
        </section>

        {/* Research Prototype Notice */}
        <section className="about-section">
          <div className="research-notice">
            <strong>Research Prototype.</strong> VEERA is an academic research project, not a
            commercial inspection product. Its assessments are experimental AI outputs and should
            not be used as substitutes for professional structural inspection. The system does not
            claim superiority over existing inspection methods — it explores how failure-aware
            evidence acquisition can improve the reliability of multimodal AI for visual tasks.
          </div>
        </section>
      </div>
    </main>
  );
}

function PipelineStep({ icon, label }) {
  return (
    <div className="pipeline__step">
      {icon}
      <span>{label}</span>
    </div>
  );
}

function PipelineArrow() {
  return <ChevronRight size={16} className="pipeline__arrow" aria-hidden="true" />;
}
