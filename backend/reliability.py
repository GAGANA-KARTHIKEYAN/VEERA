"""
VEERA — Audited Reliability, Sufficiency Gating & Failure-Aware Abstention Module

This module implements the canonical reliability and abstention formulation for VEERA:
1. Canonical Empirical Reliability Gap:
   G(x, q) = |p_Yes - p_No| in [0.0, 1.0]
   derived from full-vocabulary softmax probabilities over tokens 9454 ('Yes') and 2753 ('No').

2. Calibration Threshold:
   tau = 0.7853
   Provenance: Selected as the quantile threshold on the 954-instance validation split
   across 100 images from the RePOPE benchmark (Notebook Cell 51).
   Scientific Limitation: Validated specifically for natural-image object-presence QA
   under Qwen2.5-VL-3B-Instruct. Uncalibrated for arbitrary physical crack/defect inspection.

3. Failure-Aware Gating Principles:
   - A model prediction is NOT a verified conclusion.
   - High average confidence does not excuse a weak or contradictory localized crop.
   - Crop unanimity or a 75% majority alone is NEVER accepted as proof of correctness.
   - In any ambiguous, contradictory, or sub-threshold case, VEERA strictly abstains
     (status="review", answer="uncertain", assessment="inconclusive").
"""

import math
from typing import Tuple, Dict, Any, List, Optional

DEFAULT_TAU_THRESHOLD = 0.7853


def validate_probability(p: Any, name: str = "probability") -> float:
    """
    Validates that a probability is a real, finite float within [0.0, 1.0].
    Raises ValueError with a specific diagnostic on non-finite, negative, or > 1 values.
    """
    if p is None:
        raise ValueError(f"Missing {name}: value cannot be None.")
    try:
        val = float(p)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Malformed {name} '{p}': must be a numeric float. ({e})")

    if math.isnan(val):
        raise ValueError(f"Invalid non-finite {name}: value is NaN.")
    if math.isinf(val):
        raise ValueError(f"Invalid non-finite {name}: value is Infinite.")
    if val < 0.0 or val > 1.0:
        raise ValueError(f"Out-of-bounds {name} {val:.6f}: must be within [0.0, 1.0].")

    return val


def compute_gap_from_probabilities(p_yes: Any, p_no: Any) -> Tuple[float, str]:
    """
    Canonical VEERA Reliability Gap:
    G(x, q) = |p_Yes - p_No| in [0.0, 1.0]

    Args:
        p_yes: Vocabulary softmax probability for 'Yes' (token 9454)
        p_no:  Vocabulary softmax probability for 'No'  (token 2753)

    Returns:
        (gap: float, predicted_direction: 'yes' | 'no')
    """
    pyes = validate_probability(p_yes, "p_yes")
    pno = validate_probability(p_no, "p_no")

    # In full vocabulary softmax, sum of two tokens can be <= 1.0
    if pyes + pno > 1.00001:
        raise ValueError(
            f"Invalid probability distribution: p_yes ({pyes:.4f}) + p_no ({pno:.4f}) = {pyes + pno:.4f} > 1.0."
        )

    gap = abs(pyes - pno)
    prediction = "yes" if pyes >= pno else "no"
    return round(gap, 6), prediction


def compute_probability_gap_from_logits(
    logits_yes: Any, logits_no: Any
) -> Tuple[float, float, float, str]:
    """
    Binary-Pair Preference Softmax (Heuristic Diagnostic):
    Normalizes ONLY across the 2-element pair {Yes, No}.

    IMPORTANT MATHEMATICAL DISTINCTION:
    Binary softmax rescales relative pair preference to sum to 1.0 and does NOT
    represent full-vocabulary token probabilities. It should not be evaluated
    directly against thresholds calibrated on full-vocabulary softmax without recalibration.

    Uses numerically stable softmax: exp(x - max(x)).
    """
    if logits_yes is None or logits_no is None:
        raise ValueError("Logits cannot be None.")
    try:
        lyes = float(logits_yes)
        lno = float(logits_no)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Malformed logits: must be numeric floats ({e}).")

    if math.isnan(lyes) or math.isnan(lno) or math.isinf(lyes) or math.isinf(lno):
        raise ValueError(f"Non-finite logits encountered: ({lyes}, {lno}).")

    max_logit = max(lyes, lno)
    exp_yes = math.exp(lyes - max_logit)
    exp_no = math.exp(lno - max_logit)
    sum_exp = exp_yes + exp_no

    if sum_exp <= 0.0 or math.isinf(sum_exp) or math.isnan(sum_exp):
        raise ValueError(f"Numerical instability in binary softmax (sum_exp={sum_exp}).")

    p_yes = exp_yes / sum_exp
    p_no = exp_no / sum_exp
    gap = abs(p_yes - p_no)
    prediction = "yes" if p_yes >= p_no else "no"

    return round(p_yes, 6), round(p_no, 6), round(gap, 6), prediction


# Backward-compatible alias for existing callers
def compute_probability_gap(logits_yes: Any, logits_no: Any) -> Tuple[float, float, float, str]:
    """Alias for compute_probability_gap_from_logits for backward compatibility."""
    return compute_probability_gap_from_logits(logits_yes, logits_no)


def is_evidence_sufficient(gap: Any, threshold: Any = DEFAULT_TAU_THRESHOLD) -> bool:
    """
    Strict evidence sufficiency test:
    Returns True if and only if:
      1. Both gap and threshold are valid, finite, non-negative numbers.
      2. gap >= threshold.
    """
    try:
        g = float(gap)
        t = float(threshold)
    except (TypeError, ValueError):
        return False

    if math.isnan(g) or math.isnan(t) or math.isinf(g) or math.isinf(t):
        return False
    if g < 0.0 or t < 0.0:
        return False

    return g >= t


def evaluate_evidence_limitation(
    question: str,
    global_gap: float,
    threshold: float,
    crop_evaluations: List[Dict[str, Any]],
    image_size: Optional[Tuple[int, int]] = None,
) -> Dict[str, Any]:
    """
    Diagnoses why evidence is insufficient or contradictory and generates
    structured requests for supplemental external photographs.
    """
    clean_q = (question or "").lower().strip()
    total_crops = len(crop_evaluations) if crop_evaluations else 0

    valid_crops = [
        c for c in (crop_evaluations or [])
        if isinstance(c, dict) and c.get("vote") in {"yes", "no"}
    ]
    yes_votes = sum(1 for c in valid_crops if c.get("vote") == "yes")
    no_votes = sum(1 for c in valid_crops if c.get("vote") == "no")

    gaps = []
    for c in valid_crops:
        try:
            score = float(c.get("reliability_score", 0.0))
            if not math.isnan(score) and not math.isinf(score) and score >= 0.0:
                gaps.append(score)
        except (TypeError, ValueError):
            pass

    mean_crop_gap = sum(gaps) / len(gaps) if gaps else 0.0

    # 1. Contradictory localized evidence
    if yes_votes > 0 and no_votes > 0:
        limitation_type = "contradictory_crop_evidence"
        reason = (
            f"Localized crops produced contradictory evidence ({yes_votes} Yes vs {no_votes} No). "
            "A conflicting regional signal indicates features are ambiguous, localized, or shadowed."
        )
    # 2. Extremely low reliability signal across crops
    elif mean_crop_gap < threshold:
        limitation_type = "low_reliability_signal"
        reason = (
            f"Visual features exhibit high model uncertainty (mean reliability gap {mean_crop_gap:.2%} < threshold {threshold:.2%}). "
            "Surface texture or lighting cannot be reliably disambiguated."
        )
    # 3. Low input resolution
    elif image_size and (image_size[0] < 300 or image_size[1] < 300):
        limitation_type = "low_resolution"
        reason = (
            f"Input image resolution ({image_size[0]}x{image_size[1]}px) is insufficient to resolve fine structural details."
        )
    else:
        limitation_type = "unresolved_ambiguity"
        reason = (
            f"Global pass gap (G={global_gap:.2%}) and crop evaluations did not reach calibration threshold tau={threshold:.2%}."
        )

    # Generate tailored requested evidence options
    requested_evidence = []
    if any(k in clean_q for k in ["crack", "fracture", "damage", "scratch", "break", "split"]):
        requested_evidence = [
            {
                "type": "close_up",
                "instruction": "Please upload a closer photograph of the suspected fissure near the surface centre.",
                "rationale": "High optical detail is required to distinguish fine fractures from superficial surface markings."
            },
            {
                "type": "alternate_angle",
                "instruction": "Please photograph the surface from an oblique angle with diffuse ambient lighting.",
                "rationale": "Grazing-angle lighting reveals physical surface relief and eliminates false shadows."
            },
            {
                "type": "wider_view",
                "instruction": "Please upload a wider photograph showing the surrounding wall/surface continuation.",
                "rationale": "Context is needed to trace boundary continuity across the structure."
            }
        ]
    elif any(k in clean_q for k in ["screen", "display", "laptop", "monitor", "glass", "phone"]):
        requested_evidence = [
            {
                "type": "close_up",
                "instruction": "Please upload a close-up photograph of the suspected display damage area.",
                "rationale": "Closer detail allows distinguishing internal digitizer cracks from surface smudge."
            },
            {
                "type": "alternate_angle",
                "instruction": "Please take another photograph with reduced screen reflection and diffuse ambient lighting.",
                "rationale": "Specular reflections on glass panels create false edges and mask fracture lines."
            }
        ]
    elif any(k in clean_q for k in ["road", "pothole", "pavement", "asphalt", "concrete"]):
        requested_evidence = [
            {
                "type": "close_up",
                "instruction": "Please upload a closer image focusing on the boundary of the suspected depression.",
                "rationale": "Edge depth contrast is required to measure surface depression."
            },
            {
                "type": "wider_view",
                "instruction": "Please provide a wider view showing the surrounding road surface and pavement markings.",
                "rationale": "Surrounding lane context clarifies scale and geometry."
            }
        ]
    else:
        requested_evidence = [
            {
                "type": "close_up",
                "instruction": "Please upload a closer, higher-resolution photograph of the specific region of interest.",
                "rationale": "The current viewpoint does not show sufficient fine detail to support a definitive conclusion."
            },
            {
                "type": "alternate_angle",
                "instruction": "Please provide an alternate angle under clear, diffuse lighting.",
                "rationale": "Varying illumination angles helps eliminate ambiguous reflections and shadows."
            }
        ]

    return {
        "limitation_type": limitation_type,
        "reason": reason,
        "requested_evidence": requested_evidence,
    }


def aggregate_crop_evidence(
    crop_evaluations: List[Dict[str, Any]],
    threshold: float = DEFAULT_TAU_THRESHOLD,
    global_prediction: Optional[str] = None,
    global_gap: float = 0.0,
) -> Dict[str, Any]:
    """
    Audited Multi-Crop Evidence Aggregation and Abstention Policy:

    STRICT FAILURE-AWARE RULES:
    1. Validation of Inputs:
       - Empty crop list -> status="review", answer="uncertain", reason="No crops provided"
       - Malformed / non-finite scores -> status="review", answer="uncertain", reason="Invalid crop scores"
       - Unknown vote labels -> rejected or treated as uncertain

    2. Deadlock & Ties:
       - 2 YES / 2 NO or any tied vote -> status="review", answer="uncertain"

    3. Crop-to-Crop Contradictions:
       - 3 NO / 1 YES (The Wall-Crack Regression Case):
         A single localized crop detected a defect (crack), while 3 blank regions saw nothing.
         Majority vote alone CANNOT outvote a localized positive finding.
         VEERA strictly ABSTAINS (status="review", answer="uncertain").
       - 3 YES / 1 NO:
         Contradiction exists. Requires that all 3 positive crops independently meet threshold tau.
         If any crop has low reliability (g_i < tau), VEERA strictly ABSTAINS.

    4. Unanimous Crops with Low Reliability:
       - If all crops agree (4/4) BUT their scores are weak (min(g_i) < tau),
         unanimity is NOT proof of correctness. VEERA strictly ABSTAINS.

    5. High Mean with Weak Outlier:
       - A high mean score (e.g. 0.82) that masks a weak crop (e.g. 0.05) is rejected.
         Every crop in the consensus must individually meet min_gap >= tau.

    6. Global vs Crop Majority Conflict:
       - If global pass predicted 'yes' and crops predict 'no' (or vice versa),
         this indicates a multi-scale spatial conflict. VEERA strictly ABSTAINS.

    7. Autonomous Answer:
       - Allowed ONLY if all crops agree (100% consensus),
         every crop satisfies min_gap >= tau,
         and there is no conflict with global prediction.
    """
    # Rule 1: Empty crop list
    if not crop_evaluations:
        return {
            "status": "review",
            "answer": "uncertain",
            "mean_gap": 0.0,
            "min_gap": 0.0,
            "consensus_ratio": 0.0,
            "rationale": "No crops were provided for evidence verification. Evidence is insufficient.",
            "evidence_sufficient": False,
        }

    # Rule 1b: Validate all crops and detect corrupted / non-finite scores
    total_crops = len(crop_evaluations)
    valid_votes = []
    gaps = []
    for c in crop_evaluations:
        if not isinstance(c, dict):
            return {
                "status": "review",
                "answer": "uncertain",
                "mean_gap": 0.0,
                "min_gap": 0.0,
                "consensus_ratio": 0.0,
                "rationale": "Malformed crop evidence: elements must be dictionaries.",
                "evidence_sufficient": False,
            }
        vote = str(c.get("vote", "")).strip().lower()
        if vote not in {"yes", "no", "uncertain"}:
            return {
                "status": "review",
                "answer": "uncertain",
                "mean_gap": 0.0,
                "min_gap": 0.0,
                "consensus_ratio": 0.0,
                "rationale": f"Invalid vote label '{vote}' in crop evidence.",
                "evidence_sufficient": False,
            }
        try:
            score = float(c.get("reliability_score", 0.0))
            if math.isnan(score) or math.isinf(score) or score < 0.0 or score > 1.0:
                return {
                    "status": "review",
                    "answer": "uncertain",
                    "mean_gap": 0.0,
                    "min_gap": 0.0,
                    "consensus_ratio": 0.0,
                    "rationale": f"Corrupted or non-finite reliability score ({score}) in crop evidence.",
                    "evidence_sufficient": False,
                }
        except (TypeError, ValueError):
            return {
                "status": "review",
                "answer": "uncertain",
                "mean_gap": 0.0,
                "min_gap": 0.0,
                "consensus_ratio": 0.0,
                "rationale": "Non-numeric reliability score encountered in crop evidence.",
                "evidence_sufficient": False,
            }

        valid_votes.append(vote)
        gaps.append(score)

    yes_votes = valid_votes.count("yes")
    no_votes = valid_votes.count("no")
    uncertain_votes = valid_votes.count("uncertain")
    mean_gap = sum(gaps) / total_crops
    min_gap = min(gaps) if gaps else 0.0
    consensus_count = max(yes_votes, no_votes)
    consensus_ratio = consensus_count / total_crops
    majority_vote = "yes" if yes_votes > no_votes else ("no" if no_votes > yes_votes else "tie")

    # Rule 2: Deadlock / Tie
    if majority_vote == "tie":
        return {
            "status": "review",
            "answer": "uncertain",
            "mean_gap": round(mean_gap, 4),
            "min_gap": round(min_gap, 4),
            "consensus_ratio": consensus_ratio,
            "rationale": (
                f"Crop inspection resulted in a deadlock ({yes_votes} Yes vs {no_votes} No; mean gap {mean_gap:.2%}). "
                "Local regions provide evenly split contradictory evidence. VEERA strictly abstains to prevent false certainty."
            ),
            "evidence_sufficient": False,
        }

    # Rule 3: Crop-to-crop contradictions (e.g. 3 NO / 1 YES, 1 NO / 3 YES, or any mixed votes)
    if yes_votes > 0 and no_votes > 0:
        # 3a: The Wall-Crack Failure Case: minority detected YES while surrounding crops are NO
        if yes_votes < no_votes:
            return {
                "status": "review",
                "answer": "uncertain",
                "mean_gap": round(mean_gap, 4),
                "min_gap": round(min_gap, 4),
                "consensus_ratio": consensus_ratio,
                "rationale": (
                    f"Contradictory evidence across localized crops ({yes_votes} Yes vs {no_votes} No). "
                    f"Although NO holds a {consensus_ratio:.0%} majority, a localized positive finding was observed. "
                    "In physical defect inspection, localized anomalies cannot be safely outvoted by surrounding blank regions. "
                    f"Mean gap (G={mean_gap:.2%}) is below threshold tau={threshold:.2%}. VEERA abstains."
                ),
                "evidence_sufficient": False,
            }
        # 3b: Majority YES with minority NO
        else:
            return {
                "status": "review",
                "answer": "uncertain",
                "mean_gap": round(mean_gap, 4),
                "min_gap": round(min_gap, 4),
                "consensus_ratio": consensus_ratio,
                "rationale": (
                    f"Contradictory evidence across localized crops ({yes_votes} Yes vs {no_votes} No). "
                    f"Although YES holds a {consensus_ratio:.0%} majority, crop disagreement prevents autonomous verification. "
                    f"Mean gap (G={mean_gap:.2%}) and min gap (G={min_gap:.2%}) require human expert review."
                ),
                "evidence_sufficient": False,
            }

    # Rule 4: Presence of uncertain votes among crops
    if uncertain_votes > 0:
        return {
            "status": "review",
            "answer": "uncertain",
            "mean_gap": round(mean_gap, 4),
            "min_gap": round(min_gap, 4),
            "consensus_ratio": consensus_ratio,
            "rationale": (
                f"Crop inspection contained {uncertain_votes} uncertain local evaluation(s). "
                "Evidence across regions is incomplete. Escalated to human review."
            ),
            "evidence_sufficient": False,
        }

    # Rule 5: Global vs Local Disagreement
    if (
        global_prediction
        and global_prediction in {"yes", "no"}
        and majority_vote != global_prediction
    ):
        return {
            "status": "review",
            "answer": "uncertain",
            "mean_gap": round(mean_gap, 4),
            "min_gap": round(min_gap, 4),
            "consensus_ratio": consensus_ratio,
            "rationale": (
                f"Global overview prediction ('{global_prediction.upper()}') directly conflicts with crop consensus ('{majority_vote.upper()}'). "
                f"Multi-scale spatial conflict cannot be resolved autonomously. VEERA abstains."
            ),
            "evidence_sufficient": False,
        }

    # Rule 6: Unanimous crops with weak scores (min_gap < tau)
    # Never lower threshold to half; every agreeing crop must individually meet threshold tau
    if min_gap < threshold:
        return {
            "status": "review",
            "answer": "uncertain",
            "mean_gap": round(mean_gap, 4),
            "min_gap": round(min_gap, 4),
            "consensus_ratio": consensus_ratio,
            "rationale": (
                f"Crop evaluations are unanimous ({consensus_count}/{total_crops} '{majority_vote.upper()}'), "
                f"but at least one crop has insufficient reliability (min gap {min_gap:.2%} < threshold tau={threshold:.2%}; mean gap {mean_gap:.2%}). "
                "Unanimity alone without validated per-region certainty is not proof of correctness. VEERA abstains."
            ),
            "evidence_sufficient": False,
        }

    # Rule 7: Fully Validated Autonomous Answer (100% Unanimous, min_gap >= tau, no conflicts)
    return {
        "status": "answered",
        "answer": majority_vote,
        "mean_gap": round(mean_gap, 4),
        "min_gap": round(min_gap, 4),
        "consensus_ratio": 1.0,
        "rationale": (
            f"Multi-crop inspection resolved ambiguity with 100% unanimous agreement "
            f"({consensus_count}/{total_crops} '{majority_vote.upper()}'), where every localized crop exceeded "
            f"calibration threshold tau={threshold:.2%} (min gap {min_gap:.2%}, mean gap {mean_gap:.2%})."
        ),
        "evidence_sufficient": True,
    }
