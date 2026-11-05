# VEERA — Technical Accuracy & Patentability Review Memorandum

This memorandum provides a rigorous technical audit and patentability review of the revised **Invention Disclosure Form (IDF)** for **VEERA**, prepared for academic evaluation in the **Research Methodology (RM)** course at RV University.

---

## 1. Summary of Technical Corrections Made

| Review Area | Previous Description | Corrected Status in Revised IDF | Supporting Project Evidence |
| :--- | :--- | :--- | :--- |
| **Threshold Calibration Split** | Erroneously stated that $\tau = 0.7853$ was calibrated on a "100-sample validation split". | Corrected to state that $\tau = 0.7853$ was selected on the **954-sample validation split** (comprising 100 images) to evaluate selective prediction coverage. | Notebook Cell 51 & 52: `veera_reliability_validation.csv` evaluated on 954 validation questions. |
| **Parameter Ranges (Question 16)** | Workable ranges (e.g., $\tau \in [0.65, 0.88]$, LoRA rank $4–32$, crop counts $2–8$) were listed without clear validation status. | Workable ranges are explicitly marked as **"Proposed, unvalidated range"** or **"Not experimentally established"**. Nominal settings ($r=8, \alpha=16, \tau=0.7853$, 4 crops, $75\%$ quorum) are identified as the sole implemented configuration. | `adapter_config.json`, `reliability.py:18`, `crops.py:19-21`. |
| **Non-Obviousness & Novelty (Question 15)** | Included assertive legal claims ("technical prejudice in the art", "proven non-obviousness", "patentability under Indian law"). | Rewritten as a **preliminary technical assessment**. Outlines technical differences from standard VLM pipelines while explicitly stating that formal patentability requires a prior-art search by a registered patent professional. | Question 14 search status; Section 3(k) Guidelines for Computer-Related Inventions (CRIs). |
| **Walkthrough Scenarios (Question 11)** | Walkthrough examples read as if they were recorded experimental outputs. | Explicitly titled and framed as **"Illustrative Working Examples (Simulated Walkthroughs for Disclosure Purposes — Not Measured Experiments)"**. Logits and latencies are identified as synthetic explanatory values. | Source code procedural logic in `evidence_controller.py`. |
| **Experimental Scope & Defect Claims** | Phrasing could be misconstrued as general industrial defect / crack detection. | Explicitly and consistently states that the model was fine-tuned and evaluated on the **RePOPE binary object-presence benchmark (natural images from MS-COCO)**. States clearly that physical crack detection or industrial surface fracture inspection was not evaluated. | `experiment_summary.json`, `figure_captions_and_interpretation.txt`. |
| **Exploratory Crop Evaluation** | Cropping could be misinterpreted as proven to improve accuracy in all cases. | Reports exploratory test split findings cautiously: **12 errors corrected, 11 previously correct answers altered (net gain of only +1 on 958 test instances)**. Discloses the crop controller as an experimental prototype. | `figure4_crop_policy_outcomes.png`, `VEERA.pdf` (Pages 4, 11). |
| **Proposed Claims (Question 13)** | Included speculative claims for specialized sensor hardware pipelines and dedicated logit registers. | Refined to claim standard computing hardware (processor, memory, input interface, display). Claims are clearly designated as **"Proposed Draft Claims (Prepared for Academic Invention Disclosure; Not Legally Granted Patent Claims)"**. | `app.py`, `inference.py`, `evidence_controller.py`. |
| **Inventor & Applicant Details** | Contained placeholder emails and phone numbers that could be mistaken for real. | Replaced with clean, unambiguous `[INFORMATION REQUIRED FROM INVENTORS / APPLICANT]` markers. | Formatted for student/faculty completion. |

---

## 2. Claim-to-Code Mapping & Implementation Status

| Claim # | Claim Scope | Implementation Status | Project Source Code Reference |
| :--- | :--- | :--- | :--- |
| **Claim 1** | Multimodal computing system: Base VLM + LoRA, global pass, logit isolation, sufficiency gate ($\tau$), multi-crop trigger, abstention. | **Implemented in Software** | `backend/evidence_controller.py:run_veera_pipeline()`, `backend/reliability.py`, `backend/inference.py`. |
| **Claim 2** | Base model Qwen2.5-VL-3B-Instruct, LoRA rank $r=8$, alpha $\alpha=16$, dropout $0.05$, attention projections. | **Verified in Artifacts** | `VEERA_finetuned_release/adapter/adapter_config.json`, `experiment_summary.json`. |
| **Claim 3** | Binary token isolation: Token ID 9454 ('Yes') and Token ID 2753 ('No') under Qwen2.5-VL tokenizer. | **Verified in Code** | `backend/inference.py:28-30` (`TOKEN_ID_YES = 9454`, `TOKEN_ID_NO = 2753`). |
| **Claim 4** | Sufficiency threshold $\tau = 0.7853$ selected on 954-sample validation split. | **Verified in Code & Notebook** | `backend/reliability.py:18`; Notebook Cell 51 & 52. |
| **Claim 5** | 4 overlapping crops of size $400 \times 400$ px at $50\%$ stride ratio (Top-Left, Top-Right, Center ROI, Bottom-Right). | **Verified in Code** | `backend/crops.py:17-59` (`generate_overlapping_crops()`). |
| **Claim 6** | Consensus quorum $\ge 75\%$ for answered status; contradictory votes trigger failure-aware abstention. | **Verified in Code** | `backend/reliability.py:80-114` (`aggregate_crop_evidence()`). |
| **Claim 7** | Asynchronous RESTful API gateway exposing `/health` and `/api/v1/inspect`, and graphical client dashboard. | **Implemented in Code** | `backend/app.py:25-59`; React 19 frontend in `src/App.jsx`. *(Note: Real GPU model inference requires cloud accelerator; local CPU uses offline diagnostic mode).* |
| **Claim 8** | Computer-implemented method for failure-aware evidence acquisition and adaptive inference. | **Implemented in Software** | `backend/evidence_controller.py:run_veera_pipeline()`. |
| **Claims 9–13** | Dependent method claims (chat template formatting, validation calibration, square sub-regions, structured diagnostic trace) and non-transitory storage medium. | **Implemented in Software** | `backend/schemas.py`, `backend/inference.py`, `tests/test_backend.py` (9/9 unit tests pass). |

---

## 3. Strict Boundary: Verified Experimental Results vs. Exploratory Prototypes

### A. Verified Experimental Results:
1. **LoRA Fine-Tuning Performance (RePOPE Benchmark):**
   - Training split: 2,867 questions across 300 images (MS-COCO).
   - Validation split: 954 questions across 100 images; accuracy increased from **93.61%** (baseline) to **95.49%** (fine-tuned) — net gain +18.
   - Test split: 958 questions across 100 images; accuracy increased from **93.74%** (898/958) to **95.82%** (918/958) — net gain +20.
   - Test errors reduced from 60 to 40 (**33.3% relative error reduction**).
   - Single-pass GPU inference latency: baseline mean ~0.439s; fine-tuned mean ~0.503s on Tesla T4.
   - Training efficiency: 1 epoch, 180 optimizer steps, final running mean training loss 0.0470, peak GPU memory 7.22 GB.

### B. Exploratory Prototype Limitations:
1. **Multi-Crop Accuracy Generalization:**
   - On the held-out test split, applying the crop policy corrected 12 errors but broke 11 previously correct baseline predictions, yielding a **net gain of only +1 correct prediction** (Figure 4, `figure4_crop_policy_outcomes.png`).
   - The multi-crop policy is therefore properly disclosed as an **experimental research prototype**, not as an established, universally optimal evidence acquisition policy.
2. **Domain Boundary:**
   - The model has not been trained or evaluated on physical crack detection, structural masonry, concrete fractures, or industrial defect datasets. All claims of defect detection capability must be framed as potential future transfer domains, not verified accomplishments.
3. **Deployment Runtime:**
   - Local execution without GPU runs in an offline diagnostic mode. Real model forward passes require Kaggle GPU or an accelerator with $\ge 14\text{ GB}$ VRAM.

---

## 4. Indian Patent Law (Section 3(k) & CRI Guidelines) Compliance Notes

Under Section 3(k) of the Indian Patents Act, 1970, software and algorithm patents are subject to strict scrutiny:
- **Avoided Pitfalls:** The revised claims do not claim pure mathematical formulas, raw softmax equations, or abstract algorithms in isolation.
- **Technical Effect:** The application emphasizes the tangible technical effect of the overall computer system: dynamic compute allocation that avoids unnecessary multi-billion parameter forward passes on evidentially clear inputs, coupled with failure-aware abstention that prevents misleading automated outputs.
- **Hardware Nexus:** The claims are grounded in standard computing hardware (memory storing model weights, processor executing the gating logic, input interface, and display device).
- **Recommendation:** Prior to filing Form 1 and Form 2 before the Indian Patent Office, the complete specification should be reviewed by an Indian patent agent to ensure claim preambles align with the latest CRI examination practice.
