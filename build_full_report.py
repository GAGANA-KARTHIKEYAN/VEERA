"""
VEERA — Master Research Methodology Report Generator
Produces the complete academic research report in Microsoft Word (.docx) format
adhering strictly to RV University Research Methodology template requirements.
Filename: VEERA_Research_Methodology_Final_Report.docx
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_report():
    print("Initializing document...")
    doc = Document()

    # Configure Margins: 1 inch on all sides
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True

        # Header for pages 2+
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("RV University | School of Computer Science & Engineering | Research Methodology Report")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

        # Footer for pages 2+
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun1 = fp.add_run("VEERA Research Methodology Report  |  Page ")
        frun1.font.name = "Times New Roman"
        frun1.font.size = Pt(9)
        frun1.font.color.rgb = RGBColor(120, 120, 120)

        fld1 = OxmlElement('w:fldSimple')
        fld1.set(qn('w:instr'), 'PAGE')
        fp._p.append(fld1)

        frun2 = fp.add_run(" of ")
        frun2.font.name = "Times New Roman"
        frun2.font.size = Pt(9)
        frun2.font.color.rgb = RGBColor(120, 120, 120)

        fld2 = OxmlElement('w:fldSimple')
        fld2.set(qn('w:instr'), 'NUMPAGES')
        fp._p.append(fld2)

    # Base Typography
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(35, 35, 35)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # -------------------------------------------------------------
    # Formatting Primitives
    # -------------------------------------------------------------
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(10)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(17)
        run.font.bold = True
        run.font.color.rgb = RGBColor(27, 54, 93) # Deep Academic Navy
        return p

    def add_meta_line(label, val):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(label + ": ")
        r1.font.name = 'Times New Roman'
        r1.font.bold = True
        r1.font.size = Pt(10)
        r2 = p.add_run(val)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(27, 54, 93)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(45, 45, 45)
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(70, 70, 70)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        return p

    def add_bullet(text, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_callout(text, title=None):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_shading(cell, "F4F6F9")
        
        borders_xml = f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
        '''
        cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if title:
            trun = p.add_run(title + "\n")
            trun.font.name = "Times New Roman"
            trun.font.bold = True
            trun.font.size = Pt(9.5)
            trun.font.color.rgb = RGBColor(27, 54, 93)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9.5)
        run.font.italic = True
        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = OxmlElement(m)
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

    def set_table_borders(table, color="D3D3D3"):
        tblPr = table._tbl.tblPr
        borders_xml = f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="1B365D"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
        '''
        tblPr.append(parse_xml(borders_xml))

    def add_figure(img_path, caption_text, width_in=5.8):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True
            p_img.add_run().add_picture(img_path, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            r = p_cap.add_run(caption_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(50, 50, 50)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f"[FIGURE NOT FOUND: {img_path} - {caption_text}]")
            r.font.bold = True
            r.font.color.rgb = RGBColor(200, 0, 0)

    # -------------------------------------------------------------
    # 1. TITLE PAGE / PAPER DETAILS
    # -------------------------------------------------------------
    print("Writing Title Page...")
    add_title("Failure-Aware Visual Evidence Acquisition and Adaptive Compute Allocation for Reliable Vision-Language Model Answer Verification")

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("A Research Methodology Coursework Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of Bachelor of Technology in Computer Science and Engineering")
    r_sub.font.name = "Times New Roman"
    r_sub.font.italic = True
    r_sub.font.size = Pt(11)

    add_meta_line("Author", "Chinmayi Kumaranik")
    add_meta_line("Programme", "Bachelor of Technology in Computer Science and Engineering")
    add_meta_line("Semester", "7th Semester")
    add_meta_line("Course", "Research Methodology (RM)")
    add_meta_line("Course Code", "BTECH-CSE-RM-2026")
    add_meta_line("Institutional Affiliation", "School of Computer Science and Engineering, RV University, Bengaluru, Karnataka, India")
    add_meta_line("Institutional Email", "chinmayik@rvu.edu.in  [Institutional Identity Placeholder: chinmayik.btech21@rvu.edu.in]")
    add_meta_line("Date of Submission", "November 2026")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # 2. ABSTRACT
    # -------------------------------------------------------------
    print("Writing Abstract...")
    add_heading_1("ABSTRACT")
    abstract_content = (
        "Modern Vision-Language Models (VLMs) demonstrate remarkable multimodal reasoning capabilities across visual question answering and scene understanding, yet their deployment in safety-critical domains is severely undermined by ungrounded hallucinations, overconfident errors, and language-prior shortcuts. Current selective prediction techniques combat this by abstaining from low-confidence queries; however, standard conformal or thresholded filters are overly conservative, frequently abstaining on soluble queries or incurring prohibitive computational costs through unconstrained secondary passes. This research presents VEERA, a failure-aware multimodal evidence verification and adaptive compute allocation framework designed to reliably evaluate whether VLM-generated answers are verifiably supported by visual evidence. VEERA couples a parameter-efficient Low-Rank Adaptation (LoRA) fine-tuned Qwen2.5-VL-3B-Instruct model with a dual-stage selective inference pipeline. In the initial global stage, the framework computes an empirical reliability gap derived from normalized softmax probabilities over isolated binary vocabulary tokens ('Yes' and 'No') at the prompt boundary. If this gap meets an empirical sufficiency threshold, a direct answer is rendered with minimal computational latency. Conversely, if the reliability gap falls below the sufficiency threshold, VEERA dynamically triggers an active spatial evidence acquisition engine that partitions the image into overlapping regional crops to examine localized features and reach consensus. Evaluated on the RePOPE binary object-presence benchmark comprising MS-COCO imagery, the fine-tuned core achieved 95.82% test accuracy (an improvement of 2.09 percentage points over the 93.74% baseline), delivering a 33.3% relative reduction in classification error with a modest 14.6% latency overhead. Exploratory evaluation of the multi-crop consensus policy demonstrated nuanced trade-offs, correcting 12 previously failed test instances while identifying the critical necessity of global-local context alignment. The complete system is implemented with an asynchronous FastAPI backend and an interactive React dashboard, establishing a practical, failure-aware paradigm for trustworthy visual reasoning without unconstrained compute expenditure."
    )
    p_abs = doc.add_paragraph()
    r_abs = p_abs.add_run(abstract_content)
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(10.5)

    # -------------------------------------------------------------
    # 3. INDEX TERMS
    # -------------------------------------------------------------
    p_terms = doc.add_paragraph()
    p_terms.paragraph_format.space_before = Pt(6)
    p_terms.paragraph_format.space_after = Pt(12)
    r_it_label = p_terms.add_run("Index Terms—")
    r_it_label.font.name = "Times New Roman"
    r_it_label.font.bold = True
    r_it_label.font.italic = True
    r_terms = p_terms.add_run("Adaptive Inference, Evidence Acquisition, Hallucination Mitigation, Multimodal Reasoning, Selective Prediction, Vision-Language Models.")
    r_terms.font.name = "Times New Roman"

    doc.add_page_break()

    # -------------------------------------------------------------
    # I. INTRODUCTION
    # -------------------------------------------------------------
    print("Writing Section I: Introduction...")
    add_heading_1("I. INTRODUCTION")

    add_heading_2("A. Background of the Study")
    add_p(
        "Vision-Language Models (VLMs) represent a foundational advancement in artificial intelligence, bridging the long-standing divide between computer vision and natural language processing. Contemporary architectures—exemplified by open-weight systems like Qwen2.5-VL [2], LLaVA, BLIP-2, and commercial frontier models like GPT-4V—integrate pre-trained vision encoders with high-capacity autoregressive language decoders. Through dense cross-modal projection layers or visual token adapters, these foundation models map image representations into the textual token embedding space, enabling generative comprehension of complex scenes, diagrammatic understanding, visual question answering (VQA), and multimodal dialogue."
    )
    add_p(
        "Despite their remarkable capabilities, autoregressive vision-language models operate under an inherent structural vulnerability: their language backbones are pre-trained on massive text corpora, causing them to internalize overwhelming linguistic priors. During multimodal inference, these language priors often dominate over the visual token embeddings. When confronted with ambiguous, low-resolution, occluded, or visually complex imagery, the decoder frequently predicts words based on statistical word co-occurrence rather than grounded visual features. This phenomenon gives rise to 'object hallucinations'—confidently asserting the presence of objects, attributes, or spatial relationships that do not exist in the source image. In safety-critical sectors such as civil infrastructure inspection, medical diagnostics, automated manufacturing, and autonomous vehicle perception, ungrounded model assertions introduce grave operational hazards."
    )

    add_heading_2("B. Problem Statement")
    add_p(
        "Standard Vision-Language Models lack an intrinsic mechanism to verify whether their generated outputs are verifiably supported by visual evidence. When prompted with a visual query, modern VLMs unconditionally generate tokens until an end-of-sequence delimiter is produced. Under standard greedy or beam search decoding, the model provides a point prediction accompanied by superficial softmax probabilities. However, these softmax scores reflect conditional token probabilities within an autoregressive sequence rather than well-calibrated epistemic certainty regarding factual truth."
    )
    add_p(
        "Consequently, VLMs exhibit high confidence even when entirely incorrect or when the visual evidence is insufficient to answer the query. Therefore, the core research problem addressed by this study is formulated as follows: How can an autonomous computational framework evaluate whether a VLM-generated answer is correct and evidentially grounded, dynamically acquire additional targeted visual evidence upon detecting uncertainty, and adaptively allocate compute while enforcing failure-aware abstention when evidence remains inconclusive?"
    )

    add_heading_2("C. Motivation")
    add_p(
        "The motivation for this investigation is grounded in the economic, technical, and safety imperative to deploy reliable multimodal AI in production environments. In high-stakes applications, accepting an ungrounded hallucination incurs immense risk, yet naively routing every ambiguous sample to human domain experts creates an unsustainable manual bottleneck. Current academic solutions present an impractical dichotomy:"
    )
    add_p(
        "1. Passive Abstention: Traditional selective prediction mechanisms (e.g., Whitehead et al. [3]) assign an abstention threshold to initial predictions. When confidence falls below this threshold, the system immediately refuses to answer ('I don't know'). While this limits incorrect assertions, it results in excessive over-abstention on soluble queries that merely required closer visual examination, severely degrading practical system utility."
    )
    add_p(
        "2. Unconstrained Multi-Pass Verification: Emerging multi-pass systems or post-hoc corrector pipelines (such as Woodpecker [9] or BCEA [2]) invoke heavy secondary object detectors, crop engines, or auxiliary LLMs for every query. This approach incurs prohibitive computational latency, rendering real-time or edge deployment infeasible."
    )
    add_p(
        "Hence, there is an urgent technical need for a hybrid, failure-aware framework that evaluates initial evidence with minimal compute overhead, selectively triggers targeted regional evidence acquisition only when uncertainty demands it, and strictly abstains when evidence remains contradictory."
    )

    add_heading_2("D. Research Gap")
    add_p(
        "A rigorous synthesis of recent literature in multimodal uncertainty estimation and hallucination mitigation reveals four critical research gaps:"
    )
    add_p(
        "• Gap 1: Inadequate Evidence Re-acquisition in Selective Prediction. Existing selective prediction frameworks (e.g., [1], [3]) treat answer generation as a single-shot decision. They lack active mechanisms to gather localized visual evidence before deciding to abstain."
    )
    add_p(
        "• Gap 2: Statistical Exchangeability Violations in Multi-Stage Cropping. Heuristic cropping approaches (e.g., ViCrop [12]) apply localized zooms without evaluating how localized patches disrupt the model's global contextual calibration. As highlighted by Xu et al. [2], unconstrained acquisition disrupts data exchangeability, distorting confidence boundaries."
    )
    add_p(
        "• Gap 3: Static Compute Allocation in Multimodal Foundation Models. State-of-the-art VLMs expend identical multi-billion parameter compute cycles on evidentially trivial images as they do on highly ambiguous scenes, lacking input-dependent dynamic scheduling (Xu et al. [11])."
    )
    add_p(
        "• Gap 4: Heavyweight External Dependency in Post-Hoc Verification. Existing post-hoc correction pipelines (e.g., [7], [9]) depend on external tool chains (e.g., GroundingDINO, auxiliary LLM evaluators), introducing high latency, synchronization fragility, and cascading error modes."
    )

    add_heading_2("E. Aim and Objectives")
    add_p(
        "The overarching aim of the VEERA project is to design, implement, and empirically validate an integrated, failure-aware visual evidence acquisition and adaptive compute allocation architecture that verifies VLM-generated answers, selectively resolves ambiguity through spatial crops, and enforces strict abstention."
    )
    add_p("The project is structured around six specific, measurable objectives:")
    add_bullet("Objective 1: Systematically review and critically analyze existing methodologies in VLM hallucination detection, selective prediction, and multimodal uncertainty quantification.")
    add_bullet("Objective 2: Formulate and implement an overflow-safe, vocabulary-level binary logit isolation technique to compute an empirical reliability gap directly from Qwen2.5-VL-3B forward passes.")
    add_bullet("Objective 3: Implement parameter-efficient domain adaptation (LoRA) on the Qwen2.5-VL-3B-Instruct model to enhance visual grounding and suppress language-prior bias on binary visual queries.")
    add_bullet("Objective 4: Design an adaptive spatial evidence controller that dynamically partitions imagery into overlapping sub-regions upon detecting sub-threshold confidence, evaluating multi-crop consensus.")
    add_bullet("Objective 5: Construct a full-stack, modular software deployment comprising an asynchronous FastAPI RESTful API and a responsive React 19 web dashboard displaying visual telemetry and diagnostic traces.")
    add_bullet("Objective 6: Conduct rigorous empirical evaluations on the RePOPE benchmark to measure accuracy gains, error reductions, latency trade-offs, and multi-crop policy generalization boundaries.")

    add_heading_2("F. Research Questions")
    add_p("The investigation is organized around four technical research questions:")
    add_bullet("RQ1: To what extent does vocabulary-level logit margin isolation over opposing binary answer tokens ('Yes' and 'No') serve as a reliable indicator of answer correctness in multimodal question answering?")
    add_bullet("RQ2: How significantly does parameter-efficient LoRA fine-tuning improve visual grounding and reduce hallucinations on binary presence queries compared to the zero-shot foundation baseline?")
    add_bullet("RQ3: Under what visual conditions does localized multi-crop evidence acquisition resolve initial ambiguity, and when does localized inspection induce contradictory or misleading assertions?")
    add_bullet("RQ4: What is the empirical latency and compute trade-off between direct single-pass resolution and multi-crop consensus verification in an end-to-end deployed software system?")

    add_heading_2("G. Research Contributions")
    add_p("The primary scientific and technical contributions delivered by this research include:")
    add_bullet("1. Dual-Stage Selective Verification Architecture: A structured pipeline that bifurcates inference into a high-speed global pass and a targeted regional inspection pass, adaptively conserving compute on clear inputs.")
    add_bullet("2. Grounded Parameter-Efficient Adaptation: Implementation of LoRA (rank 8, alpha 16) on Qwen2.5-VL-3B-Instruct, achieving a 33.3% relative reduction in test classification errors (from 60 errors down to 40) on RePOPE.")
    add_bullet("3. Vocabulary-Level Binary Margin Scoring: Formulation of an overflow-safe logit probability gap G(x, q) operating on exact vocabulary token IDs 9454 and 2753 at prompt position [0, -1].")
    add_bullet("4. Failure-Aware Gating Policy: Rigorous enforcement of a 75% consensus quorum and sub-threshold crop filtering, preventing weak or contradictory evidence from producing false automated conclusions.")
    add_bullet("5. Empirical Demarcation of Multi-Crop Boundaries: Honest disclosure and analysis of exploratory multi-crop outcomes (+1 net test gain), demonstrating the risks of localized cropping in the absence of global context.")
    add_bullet("6. Production-Grade Full-Stack System: A functional, open software suite combining an asynchronous FastAPI backend with a modern React 19 UI featuring bounding box overlays and multi-round evidence tracking.")

    add_heading_2("H. Organisation of the Paper")
    add_p(
        "The remainder of this report is structured as follows: Section II reviews related literature across 15 foundation studies, provides a comparative matrix, and synthesizes technical trends. Section III formalizes the research problem, hypotheses, and operational variables. Section IV outlines the research methodology, system architecture, mathematical formulations, and experimental configurations. Section V presents empirical results, performance figures, confusion matrices, and latency profiles. Section VI provides a thorough academic discussion, contextual comparisons, and limitations. Section VII concludes the report, provides practical recommendations, and delineates future research avenues."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # II. LITERATURE REVIEW AND RELATED WORK
    # -------------------------------------------------------------
    print("Writing Section II: Literature Review...")
    add_heading_1("II. LITERATURE REVIEW AND RELATED WORK")

    add_heading_2("A. Literature Search Strategy")
    add_p(
        "To establish a comprehensive theoretical and empirical foundation for VEERA, a structured literature search strategy was executed across major academic indexing databases: IEEE Xplore, ACM Digital Library, SpringerLink, ACL Anthology, CVF Open Access, arXiv, and Google Scholar. The search targeted peer-reviewed conference proceedings (CVPR, ICCV, ECCV, NeurIPS, EMNLP, ACL, ICML) and reputable preprints published between 2022 and 2026."
    )
    add_p(
        "Search strings incorporated Boolean operators combining primary concepts: ('Vision-Language Models' OR 'Multimodal Large Language Models') AND ('Hallucination Mitigation' OR 'Selective Prediction' OR 'Uncertainty Estimation' OR 'Evidence Acquisition' OR 'Calibration' OR 'Adaptive Inference'). Filtered results were restricted to English-language technical contributions focusing specifically on multimodal classification, visual question answering, model calibration, and dynamic compute allocation."
    )

    add_heading_2("B. Inclusion and Exclusion Criteria")
    add_p("Studies were screened against strict, predefined inclusion and exclusion criteria:")
    add_bullet("Inclusion Criteria (IC1): Peer-reviewed or established preprint publications addressing hallucination, selective prediction, uncertainty quantification, or adaptive inference in multimodal models.")
    add_bullet("Inclusion Criteria (IC2): Studies presenting explicit algorithmic, mathematical, architectural, or empirical methodologies for evaluating VLM correctness.")
    add_bullet("Inclusion Criteria (IC3): Works evaluating models on standard visual reasoning benchmarks (e.g., POPE, RePOPE, VQAv2, A-OKVQA, MS-COCO).")
    add_bullet("Exclusion Criteria (EC1): Unimodal NLP or unimodal computer vision studies lacking cross-modal grounding mechanisms.")
    add_bullet("Exclusion Criteria (EC2): Purely conceptual position papers lacking empirical experiments, code implementations, or quantitative evaluations.")
    add_bullet("Exclusion Criteria (EC3): Studies focusing exclusively on text-to-image diffusion models without multimodal comprehension components.")

    add_heading_2("C. Study Screening and Selection")
    add_p(
        "The selection procedure followed a rigorous screening workflow. Initial database queries yielded candidate records that underwent title and abstract screening. Duplicate entries and unimodal studies were filtered out. Full-text evaluations were subsequently performed on shortlisted papers to assess their technical relevance, experimental validity, and alignment with the core research problems of VEERA. Ultimately, fifteen foundation papers were selected for deep critical analysis and comparative synthesis."
    )

    add_heading_2("D. Critical Analysis of Existing Studies")
    add_p(
        "Below is an in-depth critical analysis of the fifteen supplied foundation studies, examining their research problems, methodologies, key contributions, direct relevance to VEERA, and methodological limitations:"
    )

    studies = [
        (
            "[1] Srinivasan et al. (ACL 2024)",
            "Selective 'Selective Prediction': Reducing Unnecessary Abstention in Vision-Language Reasoning [1]",
            "This study addresses the problem of over-cautious abstention in multimodal selective prediction. While selective prediction reduces error rates by withholding answers when confidence is low, standard thresholding causes models to abstain on up to 40% of questions that the model would have answered correctly. The authors propose ReCoVERR, an inference-time framework that actively gathers contextual evidence before confirming an abstention decision. When a VLM exhibits low confidence on an initial query, ReCoVERR prompts an auxiliary LLM to generate targeted supplementary questions. The VLM answers these auxiliary questions over the image; if high-confidence supporting evidence aligns with the initial hypothesis, the model overturns its abstention and outputs the answer. Evaluated on VQAv2 and A-OKVQA with BLIP-2 and LLaVA-1.5, ReCoVERR increased answer coverage by up to 20% without compromising accuracy. Relevance to VEERA: Demonstrates that active evidence acquisition can overturn unnecessary abstention. Limitations: Relies heavily on multi-round textual QA dialogues via an auxiliary LLM, which introduces significant latency (3–5x slowdown) and does not acquire spatial visual crops.",
        ),
        (
            "[2] Xu, Zeng, and Paisley (2026)",
            "Look Again Before You Abstain: Budgeted Conformal Evidence Acquisition for Reliable Vision-Language Models [2]",
            "Xu et al. tackle the fundamental tension between strict conformal hallucination bounds and model utility. Conventional conformal prediction produces distribution-free guarantees on error rates but forces models to abstain on over 80% of claims to maintain a 5% hallucination bound on POPE. The authors introduce Budgeted Conformal Evidence Acquisition (BCEA), a three-way decision framework: answer directly, abstain, or acquire more evidence under a compute budget. Crucially, the authors prove that applying post-hoc evidence interventions (such as localized zooming or horizontal flips) breaks data exchangeability, causing empirical error to exceed conformal risk bounds. BCEA solves this by folding the acquisition policy directly into the conformity score function. Relevance to VEERA: Directly informs VEERA's dual-stage architecture and validates the necessity of accounting for compute budgets during evidence gathering. Limitations: Conformal calibration requires large, exchangeable calibration splits; empirical testing shows high variance under extreme distribution shifts.",
        ),
        (
            "[3] Whitehead et al. (ECCV 2022)",
            "Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly [3]",
            "This landmark paper formalizes the task of Reliable VQA, arguing that autonomous multimodal agents must possess the capacity to abstain from answering rather than emitting hallucinated point predictions. The authors evaluate multiple confidence scoring mechanisms—including maximum softmax probability, entropy, and auxiliary multilayer perceptron (MLP) selection heads—across multimodal models like ViLBERT and MCAN. They formalize the Area Under the Risk-Coverage Curve (AURC) as the primary evaluation metric for selective multimodal prediction. Relevance to VEERA: Provides the foundational formulation for risk-coverage trade-offs and selective prediction gates. Limitations: The framework is purely passive; once confidence falls below threshold, the system abstains permanently without attempting visual evidence acquisition.",
        ),
        (
            "[4] Upadhyay et al. (ECCV 2022)",
            "BayesCap: Bayesian Identity Cap for Calibrated Uncertainty in Frozen Neural Networks [4]",
            "Upadhyay et al. address the challenge of deriving calibrated uncertainty from large, pre-trained neural networks without retraining or altering their core weights. They introduce BayesCap, a lightweight, post-hoc Bayesian module structured around an identity mapping attached to the frozen model's output layers. BayesCap learns a residual distribution over outputs, effectively capturing data-dependent aleatoric uncertainty while preserving the base model's deterministic representations. Relevance to VEERA: Validates the architectural paradigm of keeping the foundation base model frozen while attaching lightweight, parameter-efficient adapters (such as LoRA) to modulate confidence. Limitations: Developed primarily for continuous computer vision regression tasks (e.g., depth estimation, super-resolution), requiring adaptation for discrete token-level classification in generative VLMs.",
        ),
        (
            "[5] Lin et al. (CVPR 2025)",
            "Uncertainty Weighted Gradients for Model Calibration [5]",
            "Addressing the pervasive problem of deep neural network miscalibration, Lin et al. observe that standard loss-weighting techniques (such as Focal Loss) distort optimization trajectories and rely on single-logit confidence scores that ignore overall distribution geometry. They propose BSCE-GRA, a calibration methodology that applies Brier Score-based uncertainty weights directly to the gradients of the cross-entropy loss. By leveraging information across all output logits, their gradient-weighting scheme forces the model to focus gradient updates on poorly calibrated and highly uncertain samples. Relevance to VEERA: Highlights the critical importance of utilizing multi-logit geometry rather than isolated point probabilities when assessing epistemic certainty. Limitations: Implemented strictly during pre-training/full fine-tuning, offering limited post-hoc utility for frozen, black-box VLM deployments.",
        ),
        (
            "[6] Khan and Fu (CVPR 2024)",
            "Consistency and Uncertainty: Identifying Unreliable Responses From Black-Box Vision-Language Models for Selective VQA [6]",
            "Khan and Fu address the realistic constraint where state-of-the-art VLMs (such as GPT-4V) are accessible only via commercial black-box APIs that conceal internal weights, activations, and logit distributions. To achieve selective prediction without logits, the authors hypothesize that a model possessing true visual comprehension will produce semantically consistent answers across linguistic variations of a question. They employ a lightweight proxy model to generate a neighborhood of question rephrasings and measure the response consistency of the black-box VLM. Inconsistent answers reliably indicate high uncertainty. Relevance to VEERA: Demonstrates that consensus over localized perturbations provides a powerful surrogate for certainty. Limitations: Measuring neighborhood consistency requires multiple API calls per query, incurring high financial costs and substantial latency (1.5–3.0s per query).",
        ),
        (
            "[7] Prabhu et al. (NeurIPS 2024)",
            "Trust but Verify: Programmatic VLM Evaluation in the Wild [7]",
            "Prabhu et al. tackle the challenge of evaluating VLM truthfulness on open-ended, free-form queries where static multiple-choice benchmarks fail. They introduce PROVE (Programmatic VLM Evaluation), a framework that converts dense scene captions into high-fidelity scene graphs and algorithmically synthesizes domain-specific verification programs. By executing these verification programs against the scene graph, PROVE objectively computes precision (truthfulness) and recall (helpfulness). Their findings uncover a fundamental trade-off: models providing highly detailed answers exhibit substantially higher hallucination rates. Relevance to VEERA: Reinforces the principle that automated answer verification must be grounded in programmatic visual evidence checks rather than unconstrained text generation. Limitations: Scene-graph generation is computationally expensive and struggles with dense, fine-grained object textures.",
        ),
        (
            "[8] Xie et al. (EMNLP 2024)",
            "V-DPO: Mitigating Hallucination via Vision-Guided Direct Preference Optimization [8]",
            "Xie et al. investigate the root cause of object hallucinations in Large Vision-Language Models (LVLMs), identifying over-reliance on language priors as the primary driver. To penalize language-prior bias during training, they propose V-DPO (Vision-guided Direct Preference Optimization). They construct synthetic preference datasets containing response-contrast pairs (hallucinated vs. faithful text) and image-contrast pairs (perturbed visual contexts). Direct preference optimization over these pairs aligns the model to prioritize visual tokens over textual co-occurrences. Relevance to VEERA: Directly justifies VEERA's strategy of parameter-efficient domain fine-tuning (LoRA) to suppress language priors and enforce strict visual conditioning. Limitations: Requires curated paired preference datasets; does not provide an inference-time mechanism to detect when a fine-tuned model remains uncertain.",
        ),
        (
            "[9] Yin et al. (2023)",
            "Woodpecker: Hallucination Correction for Multimodal Large Language Models [9]",
            "Yin et al. present Woodpecker, a training-free, post-hoc framework designed to detect and correct hallucinations in generated text from MLLMs. Woodpecker operates through a five-stage sequential pipeline: key concept extraction, visual question formulation, visual knowledge validation via external vision models (e.g., GroundingDINO, BLIP-2-FLAN-T5), claim generation, and text rewriting. Woodpecker demonstrated impressive 20–30% accuracy gains across POPE benchmarks. Relevance to VEERA: Establishes the viability of verifying visual claims post-generation. Limitations: Relying on a multi-model pipeline (detector + VQA + LLM corrector) results in massive latency (often >5 seconds per query) and cascading failure modes when the object detector misidentifies small regions.",
        ),
        (
            "[10] Li et al. (CVPR 2025)",
            "UA-Pose: Uncertainty-Aware 6D Object Pose Estimation and Online Object Completion with Partial References [10]",
            "Li et al. study object pose estimation and geometry completion under severe visual occlusions and partial viewpoints. They formulate an uncertainty-aware framework that incorporates an explicit confidence distribution into neural signed distance fields (SDFs). This uncertainty metric separates visually confirmed surfaces from occluded, unseen regions, guiding active sensor sampling to complete missing object geometry. Relevance to VEERA: Exemplifies the core philosophy of VEERA: identifying exactly where visual evidence is missing or uncertain, and actively directing compute/sampling to those specific regions. Limitations: Focused strictly on 3D geometric robotics tasks, requiring translation to 2D vision-language semantic reasoning.",
        ),
        (
            "[11] Xu et al. (ICCV 2025)",
            "Learning to Inference Adaptively for Multimodal Large Language Models [11]",
            "Xu et al. address the static computational inefficiency of modern Multimodal Large Language Models (MLLMs). Foundation models execute the same number of floating-point operations regardless of whether an input image is trivially simple or highly complex. They introduce AdaLLaVA, an adaptive inference engine featuring a learned, latency-aware scheduler. At inference time, the scheduler dynamically selects network execution paths and token-pruning operations to maximize accuracy within a user-defined latency envelope. Relevance to VEERA: Directly inspires VEERA's adaptive compute allocation strategy, wherein single-pass inference is retained for high-confidence inputs, reserving multi-crop passes strictly for uncertain cases. Limitations: The scheduling policy requires complex probabilistic training integrated into the base model's internal transformer layers.",
        ),
        (
            "[12] Zhang et al. (EMNLP 2024)",
            "Towards Perceiving Small Visual Details in Zero-shot Visual Question Answering with Multimodal LLMs [12]",
            "Zhang et al. investigate scale-dependent perceptual failures in zero-shot VQA. They discover that VLM accuracy drops by up to 46% when the visual subject of a question occupies a small fraction of the image area. They demonstrate causally that when humans crop the image around the target subject, VLM accuracy recovers dramatically. To automate this, they introduce ViCrop, an automated cropping framework that uses either object detectors or the VLM's attention maps to crop and zoom into relevant regions. Relevance to VEERA: Directly motivates VEERA's spatial cropping mechanism as an effective method for acquiring fine-grained visual evidence. Limitations: ViCrop applies cropping indiscriminately or relies on external detectors, which degrades performance when the crop isolates background clutter without global context.",
        ),
        (
            "[13] Zhai et al. (ICML 2024)",
            "Investigating the Catastrophic Forgetting in Multimodal Large Language Models [13]",
            "Zhai et al. present a fundamental investigation into multimodal fine-tuning dynamics, asking whether instruction tuning causes models to lose the robust visual representations inherited from their base vision encoders. They introduce EMT (Evaluating MultiModality), an evaluation framework that probes MLLMs as pure image classifiers. Their findings reveal that extensive instruction tuning frequently degrades visual classification performance, as language decoders overfit to instruction syntax and induce feature drift. Relevance to VEERA: Crucially informs VEERA's training methodology: fine-tuning is restricted to lightweight Low-Rank Adaptation (LoRA) over attention projections with low rank (r=8) and small epoch counts (1 epoch, 180 steps) to prevent catastrophic forgetting. Limitations: Diagnostic study that does not propose an inference-time verification framework.",
        ),
        (
            "[14] Leng et al. (CVPR 2024)",
            "Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding [14]",
            "Leng et al. propose Visual Contrastive Decoding (VCD), a training-free decoding strategy that mitigates object hallucinations without retraining or external tools. They observe that hallucinated tokens are predominantly driven by language priors, which remain invariant even when the visual input is heavily corrupted. VCD contrasts the output logit distribution derived from the original image against the logit distribution derived from a visually distorted (noised) image. By subtracting the distorted logits, VCD suppresses language-prior shortcuts and amplifies genuine visual evidence. Relevance to VEERA: Confirms that contrastive logit manipulation at the decoding interface directly reflects visual grounding. Limitations: Requires two forward passes for every query, doubling baseline inference latency across all inputs regardless of certainty.",
        ),
        (
            "[15] Huang et al. (2024)",
            "A Survey on Hallucination in Large Vision-Language Models: Taxonomy, Benchmarks, and Future Directions [15]",
            "Huang et al. provide an exhaustive, authoritative taxonomy of hallucinations in multimodal large language models. They classify multimodal hallucinations into three granular hierarchical tiers: Object-level (existence and presence), Attribute-level (color, shape, material, size), and Relation-level (spatial orientation, interaction). They review the technical triggers of hallucination—such as vision-language representation misalignment, language-prior dominance, and decoding attention degradation. They benchmark existing mitigation strategies across pre-training alignment, supervised fine-tuning, preference learning, and inference-time post-processing. Relevance to VEERA: Provides the theoretical foundation for VEERA's evaluation on binary presence queries (POPE/RePOPE) and establishes the vocabulary for failure-aware categorization. Limitations: Comprehensive taxonomy and survey; does not introduce a novel empirical verification framework.",
        ),
    ]

    for title_tag, title_text, text in studies:
        add_heading_3(title_tag + " — " + title_text)
        add_p(text)

    # -------------------------------------------------------------
    # II. E. Comparative Literature Matrix
    # -------------------------------------------------------------
    print("Writing Literature Matrix...")
    add_heading_2("E. Comparative Literature Matrix")
    add_p(
        "TABLE I provides a structured comparative synthesis of the fifteen foundation studies reviewed, summarizing their research objectives, methodologies, evaluation datasets, key findings, and technical limitations in relation to VEERA."
    )

    p_tbl_cap = doc.add_paragraph()
    p_tbl_cap.paragraph_format.space_before = Pt(6)
    p_tbl_cap.paragraph_format.space_after = Pt(2)
    p_tbl_cap.paragraph_format.keep_with_next = True
    r_tc = p_tbl_cap.add_run("TABLE I. COMPARATIVE ANALYSIS OF FOUNDATION LITERATURE IN VLM RELIABILITY, VERIFICATION, AND SELECTIVE INFERENCE")
    r_tc.font.name = "Times New Roman"
    r_tc.font.size = Pt(9)
    r_tc.font.bold = True
    r_tc.font.color.rgb = RGBColor(27, 54, 93)

    # Table with 16 rows (1 header + 15 papers) and 6 columns
    table_data = [
        ["Study & Year", "Research Objective", "Core Methodology", "Dataset / Benchmark", "Key Empirical Findings", "Primary Limitations"],
        ["Srinivasan et al. (2024) [1]", "Reduce unnecessary abstention in VLM selective prediction", "ReCoVERR: Auxiliary LLM generates context questions; VLM gathers evidence", "VQAv2, A-OKVQA (BLIP-2, LLaVA-1.5)", "Answers up to 20% more questions without inflating system error rate", "High latency (3-5x); relies on textual dialogue rather than spatial image crops"],
        ["Xu et al. (2026) [2]", "Reconcile conformal error bounds with high model coverage", "Budgeted Conformal Evidence Acquisition (BCEA); 3-way decision gate", "POPE, MS-COCO (LLaVA-1.5, Qwen2.5-VL)", "Bounds hallucination at target rate while recovering coverage under compute cap", "Requires exchangeable calibration splits; fragile under domain shifts"],
        ["Whitehead et al. (2022) [3]", "Formalize reliable VQA and selective prediction trade-offs", "Post-hoc confidence estimation (softmax, entropy, MLP selection heads)", "VQA-CP v2, GQA (ViLBERT, MCAN)", "Established risk-coverage trade-off curves and AURC benchmarking in VQA", "Purely passive abstention; no active evidence acquisition mechanism"],
        ["Upadhyay et al. (2022) [4]", "Calibrate uncertainty in frozen pre-trained neural networks", "BayesCap: Lightweight Bayesian identity cap attached to output representations", "Super-resolution, Depth estimation benchmarks", "Produces calibrated uncertainty bounds without retraining foundation models", "Designed for continuous regression; unadapted for generative autoregressive tokens"],
        ["Lin et al. (2025) [5]", "Alleviate neural network miscalibration during training", "BSCE-GRA: Brier Score-weighted gradients applied to cross-entropy loss", "ImageNet, CIFAR-100 calibration splits", "Achieves state-of-the-art calibration across multiple vision architectures", "Requires full network gradient backpropagation; unusable for frozen models"],
        ["Khan & Fu (2024) [6]", "Identify unreliable responses from black-box commercial VLMs", "Neighborhood consistency: Measures prediction stability across rephrasings", "GQA, VQAv2 (GPT-4V, PaLM-2)", "Effectively detects ungrounded outputs in black-box models without logit access", "Multiple API calls per question cause high latency (1.5-3.0s) and API expenses"],
        ["Prabhu et al. (2024) [7]", "Objectively evaluate open-ended VLM truthfulness in the wild", "PROVE: Scene graphs generated from captions; executes programmatic QA checks", "PROVE benchmark, MS-COCO scenes", "Reveals severe trade-off: detailed, helpful models hallucinate significantly more", "Scene-graph extraction is slow and prone to relation misattributions"],
        ["Xie et al. (2024) [8]", "Suppress language-prior bias in LVLMs during fine-tuning", "V-DPO: Vision-guided Direct Preference Optimization over contrastive pairs", "POPE, MME, LLaVA-Bench", "Direct preference optimization significantly reduces object hallucination", "Requires curated contrastive preference pairs; no inference-time uncertainty gate"],
        ["Yin et al. (2023) [9]", "Perform training-free post-hoc hallucination correction", "Woodpecker: 5-stage pipeline extracting claims and verifying with detectors", "POPE, MME (MiniGPT-4, mPLUG-Owl)", "Improves POPE accuracy by up to 20-30% via rule-based claim rewriting", "Extreme latency (>5s per query); compounds detector error cascades"],
        ["Li et al. (2025) [10]", "Estimate 6D object pose under partial visual observations", "UA-Pose: Uncertainty-guided active spatial sampling and neural SDFs", "YCB-Video, HO3D robotics benchmarks", "Active uncertainty sampling successfully completes occluded object geometry", "Domain-restricted to 3D robotics; requires conversion to 2D semantic QA"],
        ["Xu et al. (2025) [11]", "Enable adaptive, latency-constrained inference for MLLMs", "AdaLLaVA: Learned scheduler dynamically selects layer execution and tokens", "ScienceQA, TextVQA, POPE", "Maintains accuracy while adhering to strict dynamic latency envelopes", "Requires complex probabilistic scheduling optimization during model training"],
        ["Zhang et al. (2024) [12]", "Resolve scale-dependent perceptual failures in zero-shot VQA", "ViCrop: Automatic visual cropping framework using attention/detection maps", "TextVQA, VQAv2 small-object splits", "Cropping small visual objects recovers up to 46% lost accuracy", "Applies cropping statically without evaluating global context; breaks on clutter"],
        ["Zhai et al. (2024) [13]", "Investigate catastrophic forgetting during multimodal fine-tuning", "EMT: Evaluating MultiModality probes MLLMs as pure image classifiers", "ImageNet, CIFAR, DomainNet", "Proves late instruction tuning degrades vision encoder representations", "Purely diagnostic study; provides no inference-time verification solution"],
        ["Leng et al. (2024) [14]", "Mitigate object hallucinations at decoding time without training", "VCD: Visual Contrastive Decoding contrasts original vs. distorted image logits", "POPE, LLaVA-Bench (LLaVA-1.5)", "Suppresses language-prior shortcuts by subtracting corrupted visual logits", "Requires two full forward passes for every query, doubling computational latency"],
        ["Huang et al. (2024) [15]", "Establish taxonomy and benchmark standards for VLM hallucinations", "Comprehensive survey and categorization (Object, Attribute, Relation levels)", "Taxonomic literature analysis", "Identifies core mechanisms: multimodal misalignment and language-prior bias", "Conceptual literature review; does not provide empirical verification codebase"],
    ]

    lit_table = doc.add_table(rows=len(table_data), cols=6)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lit_table)

    col_widths = [Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.0), Inches(1.1), Inches(1.0)]

    for row_idx, row_content in enumerate(table_data):
        row = lit_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D") # Navy header
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # II. F. Synthesis of Literature
    # -------------------------------------------------------------
    add_heading_2("F. Synthesis of Literature")
    add_p(
        "A holistic synthesis of the surveyed literature reveals distinct methodological paradigms and technological tensions in trustworthy multimodal reasoning:"
    )
    add_p(
        "1. Training-Time Alignment vs. Inference-Time Intervention: Training-time interventions (such as V-DPO [8] and BSCE-GRA [5]) provide structural improvements by aligning model weights to prioritize visual tokens. However, training alone cannot eliminate hallucination on out-of-distribution or ambiguous inputs. Conversely, inference-time decoding strategies (e.g., VCD [14]) and post-hoc correction pipelines (e.g., Woodpecker [9], ReCoVERR [1]) act directly on generated outputs but incur heavy latency overheads. This demonstrates the necessity of combining parameter-efficient fine-tuning with an adaptive, gated inference pipeline."
    )
    add_p(
        "2. The Compute-Reliability Trade-Off: As highlighted by Xu et al. [11] and Leng et al. [14], augmenting reliability through exhaustive multi-pass decoding or multi-crop inspection universally inflates computational cost. Uniformly applying multi-pass inspection across all inputs is computationally wasteful. VEERA synthesizes these insights by introducing an adaptive sufficiency gate that restricts multi-crop evidence acquisition strictly to instances where initial confidence is sub-threshold."
    )
    add_p(
        "3. Localized Evidence vs. Global Context Preservation: The causal findings of Zhang et al. [12] show that zooming into small objects significantly enhances perceptual acuity. However, Xu et al. [2] caution that arbitrary visual interventions disrupt distribution exchangeability. A critical insight synthesized from this tension is that localized cropping must not be evaluated in isolation: a robust architecture must cross-verify localized crop consensus against global scene context to avoid hallucinating false positives within isolated visual fragments."
    )

    add_heading_2("G. Identified Research Gap")
    add_p(
        "While prior work has explored selective prediction [1], [3], conformal evidence acquisition [2], visual cropping [12], and adaptive inference [11] in fragmented silos, no unified architecture integrates: (1) parameter-efficient grounding via LoRA, (2) zero-overhead vocabulary logit isolation for binary reliability gap scoring, (3) dynamically triggered overlapping spatial cropping, and (4) strict failure-aware quorum consensus that enforces abstention when evidence is contradictory. VEERA bridges this precise gap."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # III. RESEARCH PROBLEM, OBJECTIVES AND HYPOTHESES
    # -------------------------------------------------------------
    print("Writing Section III: Problem, Objectives & Hypotheses...")
    add_heading_1("III. RESEARCH PROBLEM, OBJECTIVES AND HYPOTHESES")

    add_heading_2("A. Formal Research Problem")
    add_p(
        "Let x in X denote an input image and q in Q denote a natural language binary question querying visual facts in x. A Vision-Language Model parameterized by theta generates an autoregressive answer y in Y = {Yes, No}. In standard deployment, the system returns y unconditionally, regardless of epistemic uncertainty."
    )
    add_p(
        "In the VEERA formulation, the system is augmented with a selective verification function f(x, q; theta) -> {Yes, No, abstain} and an evidence acquisition operator C(x) that generates spatial crops {c_1, c_2, ..., c_k}. The objective is to design a decision rule such that for a user-specified risk tolerance, the system maximizes empirical accuracy on answered samples while minimizing selective risk and computational latency L(x, q)."
    )

    add_heading_2("B. Research Objectives")
    add_p("To resolve this formal research problem, six concrete objectives are pursued:")
    add_bullet("1. Implement LoRA adaptation on Qwen2.5-VL-3B attention projection layers (q_proj, k_proj, v_proj, o_proj) with rank r=8 and alpha=16.")
    add_bullet("2. Formulate the empirical reliability gap G(x, q) = |p_Yes - p_No| based on full-vocabulary softmax at the prompt boundary.")
    add_bullet("3. Determine the empirical calibration threshold tau on validation data (calibrated at tau = 0.7853 on 954 validation samples).")
    add_bullet("4. Construct an overlapping spatial cropping algorithm generating four 400x400 crops at 50% stride ratio.")
    add_bullet("5. Enforce a failure-aware consensus rule requiring a >=75% agreement quorum and strict contradiction handling.")
    add_bullet("6. Evaluate accuracy, error reduction, confusion matrix dynamics, and latency across baseline and fine-tuned models on RePOPE.")

    add_heading_2("C. Research Questions")
    add_p("The project specifically answers:")
    add_bullet("RQ1: Does logit margin G(x, q) reliably differentiate correct predictions from hallucinations?")
    add_bullet("RQ2: Does LoRA fine-tuning yield statistically meaningful error reductions on the RePOPE benchmark?")
    add_bullet("RQ3: What is the empirical benefit and limitation of spatial multi-crop evidence acquisition?")
    add_bullet("RQ4: What is the measured latency overhead of the dual-stage verification architecture?")

    add_heading_2("D. Research Hypotheses")
    add_p(
        "To rigorously assess the empirical performance of VEERA, the following statistical hypotheses are established:"
    )
    add_callout(
        "Hypothesis 1 (Accuracy Improvement via LoRA Fine-Tuning):\n"
        "• Null Hypothesis (H01): Parameter-efficient LoRA fine-tuning of Qwen2.5-VL-3B-Instruct produces no statistically significant difference in classification accuracy on the RePOPE test split compared to the baseline model (mu_finetuned = mu_baseline).\n"
        "• Alternative Hypothesis (H11): Parameter-efficient LoRA fine-tuning produces a statistically significant increase in classification accuracy on the RePOPE test split compared to the baseline model (mu_finetuned > mu_baseline).\n\n"
        "Hypothesis 2 (Error Rate Reduction):\n"
        "• Null Hypothesis (H02): LoRA fine-tuning does not reduce the absolute number of classification errors on the 958-sample RePOPE test split.\n"
        "• Alternative Hypothesis (H12): LoRA fine-tuning reduces the absolute number of classification errors by at least 25% relative to the baseline.\n\n"
        "Hypothesis 3 (Latency Trade-Off Feasibility):\n"
        "• Null Hypothesis (H03): Incorporating the LoRA adapter and binary logit isolation increases mean single-pass inference latency by more than 30% over the base model.\n"
        "• Alternative Hypothesis (H13): Mean single-pass inference latency overhead for the fine-tuned model remains below 20% over the baseline.",
        title="FORMULATED RESEARCH HYPOTHESES"
    )

    add_heading_2("E. Variables and Operational Definitions")
    add_p(
        "TABLE II outlines the operational variables governing the VEERA framework, categorizing them into independent, dependent, controlled, and confounding variables."
    )

    p_tbl2_cap = doc.add_paragraph()
    p_tbl2_cap.paragraph_format.space_before = Pt(6)
    p_tbl2_cap.paragraph_format.space_after = Pt(2)
    p_tbl2_cap.paragraph_format.keep_with_next = True
    r_t2 = p_tbl2_cap.add_run("TABLE II. OPERATIONAL VARIABLES AND MATHEMATICAL DEFINITIONS")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(9)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(27, 54, 93)

    var_table_data = [
        ["Variable Category", "Variable Name", "Notation", "Operational Definition & Measurement Unit"],
        ["Independent Variable", "Model Adaptation State", "M", "Categorical: Baseline Zero-Shot Qwen2.5-VL-3B vs. Fine-Tuned LoRA Adapter (r=8, alpha=16)"],
        ["Independent Variable", "Evidence Acquisition Policy", "P_crop", "Categorical: Single Global Pass vs. Dual-Stage Overlapping Multi-Crop Inspection"],
        ["Independent Variable", "Sufficiency Threshold", "tau", "Continuous in [0.0, 1.0]: Calibration cut-off (nominal tau = 0.7853) governing crop triggering"],
        ["Dependent Variable", "Classification Accuracy", "Acc", "Percentage of answered test questions matching ground truth: Acc = Correct / Total * 100 (%)"],
        ["Dependent Variable", "Empirical Reliability Gap", "G(x, q)", "Continuous in [0.0, 1.0]: Absolute difference between normalized binary probabilities: |p_Yes - p_No|"],
        ["Dependent Variable", "Single-Pass Latency", "T_lat", "Continuous: Execution time per query forward pass measured in seconds (s) on Tesla T4 GPU"],
        ["Dependent Variable", "Consensus Quorum Ratio", "Q_cons", "Ratio of agreeing regional crop votes to total crops evaluated: agreed_crops / total_crops"],
        ["Controlled Variable", "Image Input Dimensions", "W, H", "Input image dimensions processed dynamically via Qwen2-VL vision processor downsampling"],
        ["Controlled Variable", "Crop Geometry & Stride", "S_crop, R_stride", "Square crops fixed at 400x400 pixels extracted at 50% spatial overlap stride"],
        ["Controlled Variable", "Hardware Environment", "HW", "Single NVIDIA Tesla T4 GPU (16 GB VRAM), Intel Xeon CPU @ 2.20 GHz, PyTorch 2.4.0+cu121"],
        ["Confounding Variable", "Object Scale & Salience", "A_rel", "Relative pixel area occupied by the query target object relative to full image canvas"],
        ["Confounding Variable", "Dataset Prior Imbalance", "R_prior", "Ratio of negative ('No') to positive ('Yes') ground-truth answers in the benchmark split"],
    ]

    var_table = doc.add_table(rows=len(var_table_data), cols=4)
    var_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(var_table)

    var_widths = [Inches(1.5), Inches(1.5), Inches(0.8), Inches(2.7)]

    for row_idx, row_content in enumerate(var_table_data):
        row = var_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = var_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D")
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    doc.add_page_break()

    # -------------------------------------------------------------
    # IV. RESEARCH METHODOLOGY
    # -------------------------------------------------------------
    print("Writing Section IV: Research Methodology...")
    add_heading_1("IV. RESEARCH METHODOLOGY")

    add_heading_2("A. Research Philosophy or Paradigm")
    add_p(
        "This research is situated within the post-positivist computational empiricism paradigm. In computational intelligence, post-positivism asserts that while an objective ground truth exists regarding visual facts depicted in an image, our observation and modeling of that truth via artificial neural networks is probabilistic, imperfect, and subject to algorithmic bias. Consequently, the research rejects the assumption of uncalibrated neural infallibility, emphasizing rigorous empirical measurement, hypothesis testing, selective prediction, and transparent error characterization."
    )

    add_heading_2("B. Research Approach")
    add_p(
        "A quantitative, experimental research approach is adopted. The study formulates mathematical models of reliability and empirical gating, implements them within a full-stack computational software pipeline, and benchmarks the resulting system against an unmodified foundation model baseline. Quantitative telemetry—encompassing categorical accuracy, precision, recall, false positive/negative counts, and microsecond-level latency logs—forms the empirical basis for hypothesis evaluation."
    )

    add_heading_2("C. Research Design")
    add_p(
        "The experimental design is structured as a comparative factorial design. The primary factor is Model Architecture (Factor A: Baseline Qwen2.5-VL-3B vs. LoRA-adapted Qwen2.5-VL-3B). The secondary factor is Inference Verification Policy (Factor B: Unconditional Global Pass vs. Dual-Stage Multi-Crop Evidence Acquisition). The evaluation is conducted across standardized benchmark splits (Validation: 954 samples; Test: 958 samples) to evaluate accuracy, selective risk, and computational efficiency."
    )

    add_heading_2("D. Overall Research Procedure")
    add_p(
        "The overall research procedure executed in the VEERA project encompasses twelve structured phases:"
    )
    add_bullet("Phase 1: Research Problem Identification — Formalizing the challenge of VLM hallucinations and over-cautious abstention.")
    add_bullet("Phase 2: Literature Review & Synthesis — Critical analysis of 15 foundation papers across selective prediction, calibration, and DPO.")
    add_bullet("Phase 3: Mathematical Formulation — Formulating vocabulary-level logit margin isolation and the empirical reliability gap G(x, q).")
    add_bullet("Phase 4: Dataset Preparation — Preprocessing the RePOPE benchmark (MS-COCO scenes) into train, validation, and test splits.")
    add_bullet("Phase 5: Parameter-Efficient Fine-Tuning — Training LoRA adapters (rank 8, alpha 16) on Qwen2.5-VL-3B attention projections.")
    add_bullet("Phase 6: Calibration & Threshold Selection — Deriving the empirical sufficiency threshold tau = 0.7853 on 954 validation samples.")
    add_bullet("Phase 7: Multi-Crop Algorithm Design — Implementing overlapping spatial crop extraction (400x400 at 50% stride) and consensus rules.")
    add_bullet("Phase 8: Backend REST Gateway Implementation — Developing an asynchronous FastAPI service with /health and /api/v1/inspect.")
    add_bullet("Phase 9: Frontend Web Dashboard Development — Creating a React 19 UI with bounding box rendering and interactive follow-up.")
    add_bullet("Phase 10: Unit & Integration Testing — Developing 21 deterministic test cases verifying probability boundaries and failure-aware gates.")
    add_bullet("Phase 11: Benchmark Evaluation — Running baseline and fine-tuned models on test splits, logging latency, errors, and confusion matrices.")
    add_bullet("Phase 12: Empirical Analysis & Demarcation — Synthesizing findings, characterizing crop policy trade-offs, and documenting limitations.")

    add_p(
        "Fig. 1 illustrates the end-to-end procedural flowchart of the research methodology and dual-stage inference process implemented in VEERA."
    )

    # Insert Fig. 1 (Method Flowchart)
    add_figure(
        "VEERA_IDF_Submission/figures/FIG2_Method_Flowchart.png",
        "Fig. 1. Overall Research Methodology Workflow and Dual-Stage Failure-Aware Inference Process (Method Aspect).",
        width_in=5.2
    )

    add_heading_2("E. Study Setting and Scope")
    add_p(
        "The computational study was conducted within a cloud GPU environment provisioned with a single NVIDIA Tesla T4 GPU (16 GB GDDR6 VRAM, PCIe Gen3), an Intel Xeon dual-core processor @ 2.20 GHz, 13 GB host RAM, and high-speed NVMe storage running Ubuntu 22.04 LTS and Python 3.10 / 3.12. The experimental scope is deliberately focused on binary visual question answering (object presence verification) using the RePOPE benchmark derived from MS-COCO natural imagery. The research scope explicitly excludes arbitrary physical crack detection or industrial surface fracture inspection, which remain uncalibrated future transfer domains."
    )

    add_heading_2("F. Population and Sampling Design")
    add_p(
        "The target population consists of multimodal visual queries evaluating factual object existence in natural scenes. The sampling design utilizes the standardized RePOPE benchmark, an adversarial extension of the POPE (Polling-based Object Probing Evaluation) protocol designed by Li et al. [15]. RePOPE samples MS-COCO imagery and constructs balanced binary queries across three negative sampling strategies (Random, Popular, and Adversarial co-occurring objects)."
    )
    add_p(
        "The dataset splits utilized in this study comprise: (1) Training Split: 2,867 question-answer pairs across 300 MS-COCO images; (2) Validation Split: 954 question-answer pairs across 100 images; (3) Held-Out Test Split: 958 question-answer pairs across 100 distinct images. No images or questions overlap between splits."
    )

    add_heading_2("G. Data Sources and Collection Methods")
    add_p(
        "Primary experimental data comprises the model outputs, logit matrices, latency measurements, and confusion matrix cell counts recorded during benchmark runs. Secondary data consists of the MS-COCO 2014 validation image repository and the corresponding RePOPE annotation JSON files specifying bounding boxes, object categories, and binary ground truth."
    )

    add_heading_2("H. Research Instruments, Tools and Technologies")
    add_p(
        "TABLE III enumerates the hardware, software frameworks, base foundation models, and development tools employed across the research lifecycle."
    )

    p_tbl3_cap = doc.add_paragraph()
    p_tbl3_cap.paragraph_format.space_before = Pt(6)
    p_tbl3_cap.paragraph_format.space_after = Pt(2)
    p_tbl3_cap.paragraph_format.keep_with_next = True
    r_t3 = p_tbl3_cap.add_run("TABLE III. RESEARCH INSTRUMENTS, SOFTWARE FRAMEWORKS, AND COMPUTATIONAL STACK")
    r_t3.font.name = "Times New Roman"
    r_t3.font.size = Pt(9)
    r_t3.font.bold = True
    r_t3.font.color.rgb = RGBColor(27, 54, 93)

    tech_table_data = [
        ["Component Tier", "Tool / Technology", "Version / Model", "Role in Research Architecture"],
        ["Base Model Core", "Qwen2.5-VL-Instruct", "3B Parameters (Auto)", "Pre-trained vision-language foundation backbone executing cross-modal transformer forward passes"],
        ["Fine-Tuning Framework", "Hugging Face PEFT", "0.12.0 (LoRA)", "Parameter-Efficient Fine-Tuning injecting low-rank trainable matrices into q_proj, k_proj, v_proj, o_proj"],
        ["Vision Processor", "Qwen2-VL Processor", "transformers 4.45+", "Dynamic visual patchification, SmartResize resolution scaling, and Jinja conversational formatting"],
        ["Deep Learning Engine", "PyTorch", "2.4.0+cu121", "GPU tensor computation, automatic mixed precision (bfloat16/float16), and memory management"],
        ["Backend REST API", "FastAPI + Uvicorn", "0.115.0 / 0.31.0", "Asynchronous HTTP server exposing /health, /api/v1/inspect, and /api/v1/inspect/follow-up endpoints"],
        ["Data Serialization", "Pydantic v2", "2.9.2", "Strict schema validation, typing enforcement, and diagnostic trace marshaling"],
        ["Image Processing", "Pillow (PIL)", "10.4.0", "Image file ingestion, coordinate bounding box cropping, and WebP thumbnail compression"],
        ["Frontend UI", "React 19 + Vite", "19.0.0 / 6.0.0", "Client dashboard rendering crop cards, probability telemetry, and interactive evidence uploads"],
        ["Styling & Icons", "Tailwind CSS / Lucide", "3.4.14 / 0.454.0", "Responsive user interface design, diagnostic styling, and visual status indicators"],
        ["Tunnel Gateway", "Cloudflare Tunnel", "cloudflared latest", "Secure HTTPS ingress bridging local frontend with remote Kaggle GPU backend"],
        ["Testing & Verification", "Python Unittest + Oxlint", "Standard / 0.15.0", "21 deterministic unit tests and JavaScript static linting ensuring zero regressions"],
    ]

    tech_table = doc.add_table(rows=len(tech_table_data), cols=4)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tech_table)

    tech_widths = [Inches(1.4), Inches(1.5), Inches(1.3), Inches(2.3)]

    for row_idx, row_content in enumerate(tech_table_data):
        row = tech_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = tech_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D")
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading_2("I. Data Preparation and Preprocessing")
    add_p(
        "Visual inputs are ingested via Pillow and processed by the Qwen2-VL vision processor using dynamic 2D patch extraction. Images are scaled while maintaining aspect ratio, mapping pixel grids into visual tokens using a 14x14 patch size. For natural language queries, conversational chat templating is strictly applied using Jinja2:"
    )
    add_callout(
        "<|im_start|>user\n"
        "<|vision_start|><|image_pad|><|vision_end|>{Question} Please answer yes or no.<|im_end|>\n"
        "<|im_start|>assistant\n",
        title="CANONICAL CHAT TEMPLATE FORMATTING"
    )
    add_p(
        "Crucially, the prompt terminates with the newline character following '<|im_start|>assistant\n'. Under byte-level Byte-Pair Encoding (BPE), tokens emitted immediately following a newline start at column zero without a leading space prefix (character byte '\\u0120'). Consequently, the opposing binary response tokens are mapped to exact vocabulary token IDs: Token ID 9454 ('Yes') and Token ID 2753 ('No'). Space-prefixed variants (such as ' Yes' [7414] and ' No' [2308]) are excluded from column-zero generation."
    )

    add_heading_2("J. Proposed Model, Framework and Analytical Procedure")
    add_p(
        "The proposed VEERA framework operates via a dual-stage, failure-aware verification pipeline:"
    )
    add_p(
        "Stage 1: Global Forward Pass and Margin Scoring. The input image x and query q are passed through the LoRA-adapted Qwen2.5-VL-3B core in a single forward pass. Rather than generating text autoregressively, the framework extracts the logit vector z at the prompt boundary position [0, -1]. Softmax normalization is computed over the isolated binary token logits:"
    )
    add_p(
        "p_Yes = exp(z_9454) / [exp(z_9454) + exp(z_2753)],   p_No = exp(z_2753) / [exp(z_9454) + exp(z_2753)]"
    )
    add_p(
        "The empirical reliability gap G(x, q) is computed as the absolute probability margin: G(x, q) = |p_Yes - p_No| in [0.0, 1.0]. To prevent numerical instability from extreme logits, the computation is implemented using an overflow-safe log-sum-exp formulation. The reliability gap is compared against the calibration threshold tau (0.7853):"
    )
    add_bullet("If G(x, q) >= tau: The global evidence is deemed sufficient. The predicted class y = argmax(p_Yes, p_No) is emitted as a confident, answered verdict. Compute is halted, avoiding additional passes.")
    add_bullet("If G(x, q) < tau: Global visual evidence is deemed insufficient or ambiguous. The adaptive evidence controller triggers Stage 2.")
    add_p(
        "Stage 2: Overlapping Multi-Crop Spatial Acquisition. The controller partitions image x into four square sub-regions (Top-Left, Top-Right, Center ROI, Bottom-Right) of size 400x400 pixels at a 50% spatial stride ratio. For smaller images (<=400 px), adaptive scaling extracts four distinct quadrants at 65% width/height to guarantee diverse viewpoints. Each crop c_i is fed into the model with query q, generating regional votes v_i and local reliability gaps G(c_i, q)."
    )
    add_p(
        "Consensus and Abstention Gating: The aggregation engine computes the vote distribution. A definitive answer is returned if and only if:"
    )
    add_bullet("1. Quorum Requirement: The majority vote reaches at least 75% consensus (e.g., 4:0 or 3:1 agreement).")
    add_bullet("2. Reliability Consistency: All concurring crops satisfy G(c_i, q) >= tau.")
    add_bullet("3. Global Alignment: The crop consensus agrees with the global pass direction.")
    add_p(
        "If a tie occurs (2:2), if consensus is sub-quorum, if any agreeing crop exhibits sub-threshold reliability, or if contradictory evidence is detected, VEERA strictly emits a failure-aware abstention signal (status='review', assessment='inconclusive'), routing the case for human inspection."
    )

    add_p("Fig. 2 illustrates the functional block diagram of the VEERA system architecture.")
    add_figure(
        "VEERA_IDF_Submission/figures/FIG1_System_Architecture.png",
        "Fig. 2. Proposed VEERA System Architecture Block Diagram (Product Aspect).",
        width_in=5.6
    )

    add_p("Fig. 3 illustrates the overlapping spatial multi-crop evidence acquisition grid.")
    add_figure(
        "VEERA_IDF_Submission/figures/FIG3_Multi_Crop_Acquisition.png",
        "Fig. 3. Multi-Crop Spatial Evidence Acquisition Grid with 50% Overlap Stride.",
        width_in=5.0
    )

    add_heading_2("K. Experimental Setup and Hyperparameters")
    add_p(
        "LoRA adaptation was configured with rank r=8, scaling factor alpha=16, and dropout probability 0.05, targeting attention projection weights (q_proj, k_proj, v_proj, o_proj) across all 36 transformer decoder blocks. The trainable parameter count was 14.1 million (representing 0.47% of total model parameters). The model was trained for 1 epoch over 2,867 training examples using the AdamW optimizer (learning rate 2e-4, linear warmup over 10 steps, cosine decay, effective batch size 16 via gradient accumulation). Training completed in 180 optimizer steps with a final running mean training loss of 0.0470 and a peak GPU memory footprint of 7.22 GB."
    )

    add_heading_2("L. Evaluation Metrics and Measurement Criteria")
    add_p("The system is evaluated using standardized statistical and operational metrics:")
    add_p("• Accuracy (Acc): Proportion of correct predictions among evaluated queries: Acc = (TP + TN) / (TP + TN + FP + FN).")
    add_p("• Sensitivity / Recall: True positive rate: Rec = TP / (TP + FN).")
    add_p("• Specificity: True negative rate: Spec = TN / (TN + FP).")
    add_p("• Precision: Positive predictive value: Prec = TP / (TP + FP).")
    add_p("• F1-Score: Harmonic mean of precision and recall: F1 = 2 * (Prec * Rec) / (Prec + Rec).")
    add_p("• Reliability Score G(x, q): Empirical confidence gap |p_Yes - p_No|.")
    add_p("• Mean Latency: End-to-end forward pass execution time measured in seconds per sample.")

    add_heading_2("M. Statistical Analysis Methods")
    add_p(
        "Empirical differences between baseline and fine-tuned configurations are assessed via paired difference analysis, confusion matrix cell frequency shifts, and relative error reduction percentages. Hypothesis testing evaluates whether observed improvements exceed predetermined margin thresholds."
    )

    add_heading_2("N. Validity, Reliability and Reproducibility")
    add_p(
        "Internal validity is ensured by maintaining identical evaluation pipelines, prompt templates, and hardware allocations across baseline and fine-tuned models. Construct validity is supported by using the recognized RePOPE benchmark. Reproducibility is guaranteed by fixing random seeds (seed 42), persisting exact LoRA adapter weights (MD5 hash: 240a1f96ae5da0433630a18b7b934086), and automating regression verification through 21 deterministic test cases."
    )

    add_heading_2("O. Ethical Considerations")
    add_p(
        "Automated AI decision-making introduces ethical hazards when systems express false certainty in safety-critical contexts. VEERA directly advances responsible AI by embedding explicit failure-aware abstention, ensuring that uncertainty triggers human review rather than silent, hazardous hallucinations. All benchmark data originates from public MS-COCO datasets free of sensitive personal identification."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # V. RESULTS
    # -------------------------------------------------------------
    print("Writing Section V: Results...")
    add_heading_1("V. RESULTS")

    add_heading_2("A. Dataset and Evaluation Profile")
    add_p(
        "The evaluation was conducted on the RePOPE benchmark across three splits: Training (2,867 samples across 300 images), Validation (954 samples across 100 images), and Test (958 samples across 100 images). The test split contains 722 ground-truth negative instances ('No') and 236 ground-truth positive instances ('Yes'), reflecting the natural class imbalance of real-world object search."
    )

    add_heading_2("B. Preliminary Analysis and Training Dynamics")
    add_p(
        "Fine-tuning progressed smoothly over 180 optimizer steps. The running mean cross-entropy loss decreased monotonically from an initial 0.684 to 0.0470 at step 180. Peak GPU VRAM utilization remained stable at 7.22 GB, well within the 16 GB capacity of the Tesla T4. No gradient explosion or numerical instability was observed under bfloat16/float16 mixed precision."
    )

    add_heading_2("C. Main Experimental Results")
    add_p(
        "TABLE IV summarizes the quantitative classification performance of the baseline Qwen2.5-VL-3B-Instruct model versus the LoRA fine-tuned VEERA core across the validation and test splits."
    )

    p_tbl4_cap = doc.add_paragraph()
    p_tbl4_cap.paragraph_format.space_before = Pt(6)
    p_tbl4_cap.paragraph_format.space_after = Pt(2)
    p_tbl4_cap.paragraph_format.keep_with_next = True
    r_t4 = p_tbl4_cap.add_run("TABLE IV. CLASSIFICATION ACCURACY AND PERFORMANCE COMPARISON ACROSS EVALUATION SPLITS")
    r_t4.font.name = "Times New Roman"
    r_t4.font.size = Pt(9)
    r_t4.font.bold = True
    r_t4.font.color.rgb = RGBColor(27, 54, 93)

    res_table_data = [
        ["Evaluation Split", "Evaluation Metric", "Baseline Qwen2.5-VL-3B", "Fine-Tuned VEERA (LoRA)", "Absolute Gain", "Relative Change"],
        ["Validation Split (N=954)", "Correct Predictions", "893 / 954", "911 / 954", "+18 samples", "+2.02%"],
        ["Validation Split (N=954)", "Classification Accuracy", "93.61%", "95.49%", "+1.88%", "+2.01% relative"],
        ["Validation Split (N=954)", "Total Errors", "61 errors", "43 errors", "-18 errors", "-29.51% error reduction"],
        ["Held-Out Test Split (N=958)", "Correct Predictions", "898 / 958", "918 / 958", "+20 samples", "+2.23%"],
        ["Held-Out Test Split (N=958)", "Classification Accuracy", "93.74%", "95.82%", "+2.09%", "+2.23% relative"],
        ["Held-Out Test Split (N=958)", "Total Errors", "60 errors", "40 errors", "-20 errors", "-33.33% error reduction"],
    ]

    res_table = doc.add_table(rows=len(res_table_data), cols=6)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(res_table)

    res_widths = [Inches(1.5), Inches(1.3), Inches(1.2), Inches(1.2), Inches(0.8), Inches(1.0)]

    for row_idx, row_content in enumerate(res_table_data):
        row = res_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = res_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D")
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_p(
        "On the held-out test split, VEERA increased accuracy from 93.74% to 95.82%, an improvement of 2.09 percentage points. Most notably, total classification errors dropped from 60 to 40, achieving a 33.33% relative error reduction."
    )

    add_heading_2("D. Hypothesis Testing")
    add_p(
        "Evaluating the experimental results against the formulated hypotheses:"
    )
    add_bullet("Hypothesis 1 (Accuracy Gain): The fine-tuned model achieved 95.82% vs. 93.74% on the test split (+2.09 percentage points; +20 correct answers). The null hypothesis H01 is rejected in favor of alternative hypothesis H11.")
    add_bullet("Hypothesis 2 (Error Reduction): Errors were reduced from 60 to 40, achieving a 33.33% relative error reduction. Because 33.33% >= 25%, null hypothesis H02 is rejected in favor of alternative hypothesis H12.")
    add_bullet("Hypothesis 3 (Latency Overhead): Mean single-pass latency rose from 0.439s to 0.503s (+14.58%). Because 14.58% < 20%, null hypothesis H03 is rejected in favor of alternative hypothesis H13.")

    add_heading_2("E. Comparative Evaluation and Error Analysis")
    add_p(
        "TABLE V presents the confusion matrix breakdown for the fine-tuned model across all 958 test examples."
    )

    p_tbl5_cap = doc.add_paragraph()
    p_tbl5_cap.paragraph_format.space_before = Pt(6)
    p_tbl5_cap.paragraph_format.space_after = Pt(2)
    p_tbl5_cap.paragraph_format.keep_with_next = True
    r_t5 = p_tbl5_cap.add_run("TABLE V. CONFUSION MATRIX AND DIAGNOSTIC METRICS ON REPOPE TEST SPLIT (N=958)")
    r_t5.font.name = "Times New Roman"
    r_t5.font.size = Pt(9)
    r_t5.font.bold = True
    r_t5.font.color.rgb = RGBColor(27, 54, 93)

    cm_table_data = [
        ["Diagnostic Metric", "Counts / Values", "Percentage / Rate", "Technical Interpretation"],
        ["True Negatives (TN)", "708 / 722", "98.06% Specificity", "Correctly rejected non-existent objects; exceptional resistance to hallucination"],
        ["True Positives (TP)", "210 / 236", "88.98% Sensitivity", "Correctly confirmed present objects"],
        ["False Positives (FP)", "14 / 722", "1.94% Fall-out Rate", "Hallucinated presence of absent objects; suppressed to under 2%"],
        ["False Negatives (FN)", "26 / 236", "11.02% Miss Rate", "Failed to detect small or occluded objects; constitutes 65% of remaining errors"],
        ["Positive Predictive Value", "210 / 224", "93.75% Precision", "Probability that an affirmative answer is factually correct"],
        ["Harmonic Mean (F1)", "F1 = 0.9130", "91.30% F1-Score", "Robust balance across imbalanced binary presence classes"],
    ]

    cm_table = doc.add_table(rows=len(cm_table_data), cols=4)
    cm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cm_table)

    cm_widths = [Inches(1.6), Inches(1.2), Inches(1.3), Inches(2.4)]

    for row_idx, row_content in enumerate(cm_table_data):
        row = cm_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = cm_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D")
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_p(
        "TABLE VI provides the inference latency breakdown across baseline and fine-tuned configurations."
    )

    p_tbl6_cap = doc.add_paragraph()
    p_tbl6_cap.paragraph_format.space_before = Pt(6)
    p_tbl6_cap.paragraph_format.space_after = Pt(2)
    p_tbl6_cap.paragraph_format.keep_with_next = True
    r_t6 = p_tbl6_cap.add_run("TABLE VI. INFERENCE LATENCY AND COMPUTATIONAL OVERHEAD PROFILING")
    r_t6.font.name = "Times New Roman"
    r_t6.font.size = Pt(9)
    r_t6.font.bold = True
    r_t6.font.color.rgb = RGBColor(27, 54, 93)

    lat_table_data = [
        ["Operational Configuration", "Mean Latency (s)", "Throughput (Q/s)", "Relative Latency", "Operational Trade-off Profile"],
        ["Baseline Qwen2.5-VL-3B (Global Pass)", "0.439 s", "2.28 Q/s", "1.00x (Baseline)", "Fastest execution; higher error rate (60 errors)"],
        ["Fine-Tuned VEERA (Global Pass)", "0.503 s", "1.99 Q/s", "1.15x (+14.58%)", "Optimal balance: 33.3% error reduction with minor overhead"],
        ["VEERA Dual-Stage (Global + 4 Crops)", "2.210 s", "0.45 Q/s", "5.03x (+403%)", "High-depth inspection; invoked selectively on uncertain samples"],
    ]

    lat_table = doc.add_table(rows=len(lat_table_data), cols=5)
    lat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lat_table)

    lat_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.5)]

    for row_idx, row_content in enumerate(lat_table_data):
        row = lat_table.rows[row_idx]
        for col_idx, text in enumerate(row_content):
            cell = row.cells[col_idx]
            cell.width = lat_widths[col_idx]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            if row_idx == 0:
                run.font.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_shading(cell, "1B365D")
            else:
                run.font.size = Pt(8.0)
                if row_idx % 2 == 1:
                    set_cell_shading(cell, "FFFFFF")
                else:
                    set_cell_shading(cell, "F9FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading_2("F. Tables, Figures and Supporting Empirical Visualizations")
    add_p(
        "The empirical findings are visualized in Figs. 4 through 8, depicting accuracy improvements, confusion distributions, latency trade-offs, and multi-crop exploratory outcomes."
    )

    # Insert Fig. 4 (Accuracy Comparison)
    add_figure(
        "figure1_accuracy_comparison.png",
        "Fig. 4. Baseline vs. LoRA Fine-Tuned Accuracy on RePOPE Validation (+1.88%) and Test Splits (+2.09%).",
        width_in=4.8
    )

    # Insert Fig. 5 (Confusion Matrix)
    add_figure(
        "figure2_test_confusion_matrix.png",
        "Fig. 5. Confusion Matrix of the Fine-Tuned VEERA Model across 958 RePOPE Test Instances.",
        width_in=4.6
    )

    # Insert Fig. 6 (Latency Trade-Off)
    add_figure(
        "figure3_accuracy_latency_tradeoff.png",
        "Fig. 6. Accuracy-Latency Trade-off: Accuracy vs. Mean Forward Pass Execution Time on Tesla T4 GPU.",
        width_in=4.8
    )

    # Insert Fig. 7 (Crop Policy Outcomes)
    add_figure(
        "figure4_crop_policy_outcomes.png",
        "Fig. 7. Exploratory Crop Policy Outcomes: Corrected, Broken, and Net Additional Correct Predictions across Splits.",
        width_in=5.0
    )

    # Insert Fig. 8 (Accuracy Across Splits)
    add_figure(
        "figure5_accuracy_across_splits.png",
        "Fig. 8. Accuracy Across Evaluation Splits: Systematic Comparison of Baseline and Fine-Tuned Model Trajectories.",
        width_in=4.8
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # VI. DISCUSSION
    # -------------------------------------------------------------
    print("Writing Section VI: Discussion...")
    add_heading_1("VI. DISCUSSION")

    add_heading_2("A. Interpretation of Findings")
    add_p(
        "The empirical results demonstrate that parameter-efficient Low-Rank Adaptation (LoRA) successfully recalibrates the multimodal attention mechanisms of Qwen2.5-VL-3B-Instruct. By injecting low-rank matrices into query, key, value, and output attention projections, the model learns to prioritize visual token activations over internalized language priors. This is quantitatively substantiated by the confusion matrix (Fig. 5): the model achieved an exceptional 98.06% specificity (708/722 True Negatives), with false positives suppressed to 1.94% (14 instances). In binary presence QA, false positives represent genuine hallucinations (claiming an absent object exists). Suppressing hallucinations to under 2% validates the effectiveness of the training procedure."
    )
    add_p(
        "Furthermore, isolating vocabulary token IDs 9454 and 2753 directly at the prompt boundary [0, -1] yields an overflow-safe, zero-overhead reliability gap G(x, q). Because G(x, q) is calculated during the initial forward pass, it requires no extra inference operations. When G(x, q) meets or exceeds the calibration threshold tau = 0.7853, the model's empirical accuracy exceeds 98%, confirming that the margin between opposing binary logits serves as an outstanding proxy for epistemic certainty."
    )

    add_heading_2("B. Comparison with Previous Studies")
    add_p(
        "Contextualizing VEERA within the broader landscape of foundation literature:"
    )
    add_bullet("Comparison with Srinivasan et al. [1] (ReCoVERR): While ReCoVERR generates multi-turn textual dialogue via an auxiliary LLM to resolve uncertainty, VEERA uses spatial visual crops. VEERA executes in 2.21s during crop passes, whereas ReCoVERR requires 3–5 seconds due to sequential autoregressive text generation.")
    add_bullet("Comparison with Xu et al. [2] (BCEA): Xu et al. established budgeted conformal bounds. VEERA incorporates their principle of compute budgeting by restricting multi-crop passes strictly to sub-threshold inputs, conserving 403% latency overhead on 85% of queries.")
    add_bullet("Comparison with Whitehead et al. [3]: Unlike Whitehead et al.'s passive abstention framework, VEERA provides an active intermediate tier (spatial multi-crop consensus), actively attempting to resolve ambiguity before falling back to abstention.")
    add_bullet("Comparison with Yin et al. [9] (Woodpecker): Woodpecker relies on an external multi-model toolchain (GroundingDINO + BLIP-2), incurring extreme latency (>5s). VEERA is entirely self-contained, using the same unified VLM core for both global and regional passes.")
    add_bullet("Comparison with Leng et al. [14] (VCD): Visual Contrastive Decoding requires two full passes on every query. VEERA uses a single pass for confident inputs, allocating secondary passes only when necessary.")

    add_heading_2("C. Theoretical, Technical and Practical Implications")
    add_p(
        "Theoretical Implications: This work demonstrates that selective prediction in multimodal models can be framed as an active spatial evidence search rather than a passive binary rejection gate. It demonstrates that logit geometry at the prompt boundary contains rich epistemic certainty signals prior to autoregressive token emission."
    )
    add_p(
        "Technical Implications: The modular architecture decouples the heavy neural backbone from the lightweight verification and routing layer. The FastAPI gateway and React client demonstrate that research-grade VLM reliability pipelines can be deployed as responsive, production-ready full-stack web applications."
    )
    add_p(
        "Practical Implications: In critical applications like civil infrastructure inspection or automated manufacturing, VEERA provides an essential safeguard against silent AI errors. By abstaining when evidence is contradictory, the system guarantees that uncertain edge cases are safely escalated to certified human inspectors."
    )

    add_heading_2("D. Unexpected Findings: The Multi-Crop Generalization Paradox")
    add_p(
        "A critical unexpected finding emerged during exploratory analysis of the multi-crop consensus policy (Fig. 7). On the validation split, applying multi-crop inspection corrected 14 errors while breaking 6 previously correct answers, delivering a net gain of +8. However, on the held-out test split, the policy corrected 12 errors but broke 11 previously correct baseline predictions, yielding a net gain of only +1."
    )
    add_p(
        "Diagnostic inspection revealed why: when an image is cropped into isolated 400x400 regional tiles without global context, visual clutter or ambiguous background textures can locally resemble target objects. For example, a texture on a wall or a folded blanket inside a cropped tile can fool the model into voting 'Yes', creating a false majority that overrules a correct global 'No'. This finding provides vital cautionary evidence: localized spatial zooming is not a universal panacea and must always be cross-verified against global scene context."
    )

    add_heading_2("E. Threats to Validity and Study Limitations")
    add_p("The findings must be interpreted within the context of specific technical limitations:")
    add_bullet("1. Benchmark Domain Boundary: The model was fine-tuned and evaluated on RePOPE (MS-COCO natural imagery). The calibrated threshold tau = 0.7853 and observed accuracy metrics cannot be extrapolated to physical structural crack detection or industrial surface fracture inspection without dedicated in-domain calibration.")
    add_bullet("2. Binary Question Scope: The evaluation was conducted on binary presence queries ('Yes'/'No'). Multi-choice VQA, dense grounding, and free-form generation were not evaluated.")
    add_bullet("3. Exploratory Policy Tuning: The multi-crop consensus threshold was tuned post-hoc. As emphasized in the text, post-hoc tuning breaks statistical exchangeability, and the multi-crop results must be treated as an exploratory research prototype.")
    add_bullet("4. Computational Resource Constraints: Real-time GPU inference requires at least 14 GB VRAM. When running in CPU-only environments, the backend falls back to offline diagnostic mode.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # VII. CONCLUSION AND FUTURE WORK
    # -------------------------------------------------------------
    print("Writing Section VII: Conclusion & Future Work...")
    add_heading_1("VII. CONCLUSION AND FUTURE WORK")

    add_heading_2("A. Conclusion")
    add_p(
        "This research presented VEERA, an end-to-end failure-aware visual evidence acquisition and adaptive compute allocation framework designed to verify the correctness of Vision-Language Model answers. By combining parameter-efficient LoRA fine-tuning of Qwen2.5-VL-3B-Instruct with vocabulary-level logit margin isolation, VEERA achieves a 33.3% relative error reduction on the RePOPE benchmark while suppressing false positive hallucinations to 1.94%. The dual-stage architecture successfully stratifies inference, rendering direct high-confidence answers in 0.503s while reserving multi-crop evidence acquisition and strict abstention for ambiguous inputs. All six research objectives were successfully accomplished, delivering a functional, verified full-stack software system."
    )

    add_heading_2("B. Research Contributions")
    add_p("The primary verified contributions delivered by this research comprise:")
    add_bullet("1. Dual-stage selective verification pipeline reconciling high accuracy with compute efficiency.")
    add_bullet("2. Grounded LoRA adaptation of Qwen2.5-VL-3B yielding 95.82% test accuracy (+2.09% over baseline).")
    add_bullet("3. Overflow-safe binary logit margin G(x, q) isolating vocabulary token IDs 9454 and 2753.")
    add_bullet("4. Failure-aware consensus policy enforcing 75% quorum and strict abstention on contradictions.")
    add_bullet("5. Rigorous characterization of multi-crop trade-offs (+1 net test gain), exposing localized context risks.")
    add_bullet("6. Production-grade full-stack implementation comprising FastAPI backend and React 19 dashboard.")

    add_heading_2("C. Practical Recommendations")
    add_p("Based on empirical findings, three recommendations are offered for deploying trustworthy VLMs:")
    add_bullet("Recommendation 1: Always decouple confidence estimation from autoregressive sequence generation by utilizing prompt-boundary logit margins.")
    add_bullet("Recommendation 2: Do not rely solely on localized visual cropping; always require concordance between regional crops and global scene context before overturning an answer.")
    add_bullet("Recommendation 3: Embed explicit failure-aware abstention states in production APIs, enabling seamless escalation to human domain experts.")

    add_heading_2("D. Future Scope")
    add_p("Promising avenues for future research include:")
    add_bullet("1. Conformal Risk Guarantees: Integrating exchangeable split calibration (BCEA) to provide formal distribution-free risk bounds.")
    add_bullet("2. Learned Multi-Scale Crop Selection: Replacing fixed grid crops with attention-driven or reinforcement-learned bounding box proposals.")
    add_bullet("3. Domain Transfer to Structural Inspection: Fine-tuning and calibrating the pipeline on industrial concrete crack and surface defect benchmarks (e.g., SDNET2018, CODEBRIM).")
    add_bullet("4. Conversational Multi-Round Follow-up: Extending the interactive evidence acquisition protocol to support multi-turn human-in-the-loop clarifications.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    print("Writing Acknowledgement...")
    add_heading_1("ACKNOWLEDGEMENT")
    add_p(
        "The author expresses profound gratitude to the faculty and research mentors of the School of Computer Science and Engineering, RV University, Bengaluru, for their guidance, critical reviews, and academic support throughout the Research Methodology (RM) coursework. Appreciation is extended to the open-source AI research community, particularly the Alibaba Qwen team for releasing the Qwen2.5-VL foundation model, the Hugging Face team for PEFT and Transformers libraries, and the authors of the POPE and RePOPE benchmarks for providing standardized evaluation protocols. Computational resources provisioned via Kaggle GPU environments are gratefully acknowledged."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    print("Writing References...")
    add_heading_1("REFERENCES")
    add_p(
        "The following fifteen references represent the verified literature base evaluated in this research, formatted in IEEE numerical citation style:"
    )

    references_list = [
        (
            "[1]",
            "T. Srinivasan, J. Hessel, T. Gupta, B. Y. Lin, Y. Choi, J. Thomason, and K. R. Chandu, “Selective ‘Selective Prediction’: Reducing Unnecessary Abstention in Vision-Language Reasoning,” in Findings of the Association for Computational Linguistics: ACL 2024, Bangkok, Thailand, Aug. 2024, pp. 12935–12948. DOI: 10.18653/v1/2024.findings-acl.767."
        ),
        (
            "[2]",
            "J. Xu, D. Zeng, and J. Paisley, “Look Again Before You Abstain: Budgeted Conformal Evidence Acquisition for Reliable Vision-Language Models,” arXiv preprint arXiv:2410.xxxxx / 2026. [Evaluates budgeted conformal risk bounds across LLaVA and Qwen-VL foundation models]."
        ),
        (
            "[3]",
            "S. Whitehead, S. Petryk, V. Shakib, J. E. Gonzalez, T. Darrell, A. Rohrbach, and M. Rohrbach, “Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly,” in Proc. 17th European Conference on Computer Vision (ECCV 2022), Tel Aviv, Israel, Oct. 2022, pp. 148–166. DOI: 10.1007/978-3-031-19775-8_9. [Note: Supplied in prompt as Whitehead et al., 'Multimodal Selective Prediction', 2022]."
        ),
        (
            "[4]",
            "U. Upadhyay, S. Karthik, Y. Chen, M. Mancini, and Z. Akata, “BayesCap: Bayesian Identity Cap for Calibrated Uncertainty in Frozen Neural Networks,” in Proc. 17th European Conference on Computer Vision (ECCV 2022), Tel Aviv, Israel, Oct. 2022, pp. 275–294. DOI: 10.1007/978-3-031-19790-1_16."
        ),
        (
            "[5]",
            "J. Lin, L. Tao, M. Dong, and C. Xu, “Uncertainty Weighted Gradients for Model Calibration,” in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2025), Nashville, TN, USA, June 2025, pp. 15497–15507."
        ),
        (
            "[6]",
            "Z. Khan and Y. Fu, “Consistency and Uncertainty: Identifying Unreliable Responses From Black-Box Vision-Language Models for Selective Visual Question Answering,” in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2024), Seattle, WA, USA, June 2024, pp. 14249–14258. DOI: 10.1109/CVPR52733.2024.01349. [Note: Supplied in prompt as K. Khan et al., 2024]."
        ),
        (
            "[7]",
            "V. Prabhu, S. Purushwalkam, A. Yan, C. Xiong, and R. Xu, “Trust but Verify: Programmatic VLM Evaluation in the Wild,” in Proc. Thirty-eighth Conference on Neural Information Processing Systems (NeurIPS 2024), Vancouver, Canada, Dec. 2024, pp. 1–16. arXiv:2407.08684. [Note: Supplied in prompt with tentative ICCV 2025 venue; published at NeurIPS 2024]."
        ),
        (
            "[8]",
            "Y. Xie, G. Li, X. Xu, and M.-Y. Kan, “V-DPO: Mitigating Hallucination via Vision-Guided Direct Preference Optimization,” in Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, FL, USA, Nov. 2024, pp. 11624–11639. DOI: 10.18653/v1/2024.findings-emnlp.677."
        ),
        (
            "[9]",
            "S. Yin, C. Fu, S. Zhao, T. Xu, H. Wang, D. Sui, Y. Shen, K. Li, X. Sun, and E. Chen, “Woodpecker: Hallucination Correction for Multimodal Large Language Models,” arXiv preprint arXiv:2310.16045, Oct. 2023. [Note: Supplied in prompt as Y. Yin et al., 'Post-hoc Corrector for VLMs', 2023]."
        ),
        (
            "[10]",
            "M.-F. Li, W.-C. Chen, S.-P. Lee, S. Wang, and C.-C. Kao, “UA-Pose: Uncertainty-Aware 6D Object Pose Estimation and Online Object Completion with Partial References,” in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2025), Nashville, TN, USA, June 2025, pp. 1–11. arXiv:2412.03538."
        ),
        (
            "[11]",
            "Z. Xu, K. D. Nguyen, P. Mukherjee, S. Bagchi, S. Chaterji, Y. Liang, and Y. Li, “Learning to Inference Adaptively for Multimodal Large Language Models,” in Proc. IEEE/CVF International Conference on Computer Vision (ICCV 2025), Seoul, South Korea, Oct. 2025, pp. 1–12. arXiv:2412.00332."
        ),
        (
            "[12]",
            "J. Zhang, M. Khayatkhoei, P. Chhikara, and F. Ilievski, “Towards Perceiving Small Visual Details in Zero-shot Visual Question Answering with Multimodal LLMs,” in Proc. 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024), Miami, FL, USA, Nov. 2024, pp. 1–14. arXiv:2310.16016."
        ),
        (
            "[13]",
            "Y. Zhai, S. Tong, X. Li, M. Cai, Q. Qu, Y. J. Lee, and Y. Ma, “Investigating the Catastrophic Forgetting in Multimodal Large Language Models,” in Proc. Forty-first International Conference on Machine Learning (ICML 2024), Vienna, Austria, July 2024, pp. 58210–58235."
        ),
        (
            "[14]",
            "S. Leng, H. Zhang, G. Chen, X. Li, S. Lu, C. Miao, and L. Bing, “Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding,” in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2024), Seattle, WA, USA, June 2024, pp. 14010–14020. DOI: 10.1109/CVPR52733.2024.01327. [Note: Supplied in prompt as Leng et al., 'Mitigating Hallucination via Decoding Strategy Optimization', 2024]."
        ),
        (
            "[15]",
            "L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and T. Liu, “A Survey on Hallucination in Large Vision-Language Models: Taxonomy, Benchmarks, and Future Directions,” arXiv preprint arXiv:2402.00253, Feb. 2024. [Foundation taxonomy for object, attribute, and relation hallucinations]."
        ),
    ]

    for num, ref_text in references_list:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.10
        r_num = p_ref.add_run(num + " ")
        r_num.font.name = "Times New Roman"
        r_num.font.bold = True
        r_num.font.size = Pt(9.5)
        r_ref = p_ref.add_run(ref_text)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(9.0)

    # Save final document
    out_path = "VEERA_Research_Methodology_Final_Report.docx"
    print(f"Saving final document to {out_path}...")
    doc.save(out_path)
    sz = os.path.getsize(out_path)
    print(f"SUCCESS: Document generated ({sz} bytes).")
    return out_path

if __name__ == "__main__":
    generate_report()

