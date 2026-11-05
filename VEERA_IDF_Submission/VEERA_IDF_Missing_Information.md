# VEERA — Invention Disclosure Form: Missing Information Checklist

This checklist details every unresolved institutional, legal, and technical item that the student inventors, faculty supervisor, and applicant entity must confirm or supply before the **Invention Disclosure Form (IDF)** is submitted to the institutional Intellectual Property (IP) Cell at RV University or to patent counsel.

---

## 1. Inventor Details & Legal Attestation (Page 2, Question 2)

Under the Indian Patents Act, 1970, an inventor must be a natural person who contributed directly to the inventive concept, technical architecture, or algorithmic formulation.

### Inventor 1 (Lead Student Researcher / Core Architecture)
- [ ] **Full Legal Name:** *(As per official government identification / Aadhaar / Passport)*
- [ ] **Designation & Academic Roll Number:** *(e.g., B.Tech Student, Roll No. `1RVU23CSE162`)*
- [ ] **Department & School:** *(e.g., Department of Computer Science & Engineering, School of CSE)*
- [ ] **Institution:** *(RV University, Bengaluru, Karnataka, India)*
- [ ] **Contact Number:** *(Active phone number with country code `+91`)*
- [ ] **Official & Personal Email IDs:** *(University email and personal email)*
- [ ] **Nationality & Country of Residence:** *(e.g., Indian, India)*
- [ ] **Permanent Residential Postal Address:** *(Full postal address with 6-digit PIN code)*
- [ ] **Physical Signature & Date:** *(Must be signed on the printed submission copy)*

### Inventor 2 (Co-Student Researcher / Teammate)
- [ ] **Full Legal Name:** *(As per official identification)*
- [ ] **Designation & Academic Roll Number:** *(e.g., B.Tech CSE Student, Roll Number)*
- [ ] **Department & School:** *(Department of Computer Science & Engineering)*
- [ ] **Institution:** *(RV University)*
- [ ] **Contact Number:** *(Active phone number)*
- [ ] **Official Email ID:** *(University email address)*
- [ ] **Nationality:** *(e.g., Indian)*
- [ ] **Permanent Residential Postal Address:** *(Full postal address with PIN code)*
- [ ] **Physical Signature & Date:**

### Inventor 3 (Faculty Guide / Academic Supervisor)
- [ ] **Full Legal Name:** *(Faculty Guide name as per institutional records)*
- [ ] **Designation:** *(e.g., Assistant Professor / Associate Professor / Professor)*
- [ ] **Department & School:** *(Department of Computer Science & Engineering, School of CSE)*
- [ ] **Institution:** *(RV University, Bengaluru)*
- [ ] **Contact Number:** *(Official phone number)*
- [ ] **Official Institutional Email ID:** *(University faculty email)*
- [ ] **Nationality:** *(e.g., Indian)*
- [ ] **Official / Permanent Postal Address:** *(Department address or residential address)*
- [ ] **Physical Signature & Date:**

### Additional Contributors
- [ ] **Confirm Inventor Roster:** Confirm whether any other faculty member, research assistant, or student contributed to the LoRA fine-tuning, threshold calibration, or evidence controller. If yes, add their full details.

---

## 2. Public Disclosure Audit (Page 3, Question 6)

Under Sections 29–34 of The Patents Act, 1970, prior public disclosure anywhere in the world prior to the patent filing date destroys novelty, subject only to narrow statutory grace-period exceptions under Section 31.

- [ ] **Kaggle Visibility Status:**
  - Dataset: `gaganakp/veera-finetuned-release`
  - Kernel: `veera-kaggle-gpu-deployment`
  - **Action Required:** Verify whether the dataset and notebook visibility on Kaggle is currently set to **Private** or **Public**. If public, record the exact date and timestamp when visibility became public.
- [ ] **GitHub / Code Repositories:** Confirm whether any part of the project code, notebook, or LoRA adapter has been pushed to a public GitHub/GitLab repository.
- [ ] **Preprints / Publications:** Confirm whether any manuscript or abstract has been submitted to arXiv, ResearchGate, or an academic conference.
- [ ] **Academic Presentations:** Confirm whether internal course presentations (CIE) were attended by external visitors or third parties without an institutional Non-Disclosure Agreement (NDA).

---

## 3. Applicant Identity & Ownership Allocation (Page 5, Question 1)

The **Applicant** is the legal entity or natural person that will hold legal ownership of the patent rights.

- [ ] **Determine Ownership Structure:**
  - **Option A (Sole University Ownership):** RV University is named as the sole applicant. Student and faculty inventors assign rights to the university in exchange for institutional prosecution funding and academic credit under university IPR rules.
  - **Option B (Joint Ownership):** RV University and the student/faculty inventors are joint applicants.
  - **Option C (Student-Owned):** Student inventors apply in their personal capacities (requires an institutional No Objection Certificate - NOC).
- [ ] **Supply Authorized Signatory Information (if University is Applicant):**
  - Full Name of Authorized Officer: *(e.g., Registrar / Dean of Research / Director of R&D)*
  - Official Designation:
  - University Registration / Statutory Incorporation Reference:
  - Official Postal Address: *(RV University, RV Vidyaniketan Post, Mysuru Road, Bengaluru, Karnataka 560059)*
  - Official Email and Contact Number:

---

## 4. Project Funding & Contractual Declarations (Page 3, Questions 3 & 4)

- [ ] **Funding Status:** Confirm whether the project was strictly unfunded curriculum coursework for Research Methodology (RM) or received any financial grant *(e.g., RVU Seed Grant, AICTE, DST, or industry sponsor)*.
- [ ] **If Grant Funded:** Supply Grant Agency Name, Sanction Order No., Sanction Date, Project ID, and confirm whether the funder claims an IP lien.
- [ ] **Third-Party Contractual Restrictions:** Confirm whether any data, code, or images were obtained under an NDA or vendor license agreement.

---

## 5. Technical Parameter & Scope Confirmation (Page 4, Question 16)

- [ ] **Threshold Calibration ($\tau = 0.7853$):** Confirm that $\tau = 0.7853$ was selected on the 954-sample validation split to achieve a target coverage level on RePOPE natural images, and that any workable range (e.g., $0.65$ to $0.88$) remains proposed and unvalidated.
- [ ] **Target Domain Scope:** Acknowledge that the 95.82% test accuracy was measured on natural images from the RePOPE object-presence benchmark (MS-COCO objects), and that physical crack or industrial defect detection has not been evaluated.
