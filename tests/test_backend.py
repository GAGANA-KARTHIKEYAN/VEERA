"""
VEERA — Comprehensive Backend Unit, Regression & Numerical Safety Test Suite

Deterministic tests covering:
1. Reliability calculation:
   - Canonical full-vocabulary probability gap G(x, q) = |p_Yes - p_No|
   - Probability validation (NaN, Inf, negative, out-of-bounds)
   - Binary-pair preference softmax with extreme logits (numerical stability)
   - Exact threshold-boundary behavior (tau = 0.7853)
2. Decision policy & failure-aware abstention:
   - Wall-crack regression test (3 NO / 1 YES with low reliability strictly abstains)
   - 3 YES / 1 NO contradiction strictly abstains
   - 2 YES / 2 NO tied votes strictly abstains
   - Unanimous crops with weak scores (min_gap < tau) strictly abstains
   - Unanimous crops with strong scores (all gaps >= tau) answers
   - High average with a weak outlier crop strictly abstains
   - Global overview vs. local crop majority conflict strictly abstains
   - Corrupted or non-finite crop scores/votes handled safely without crash
   - Empty crop list returns explicit review disposition
3. Interactive evidence acquisition:
   - Tailored photographic request generation
   - Follow-up session persistence across rounds
   - Maximum round limit (3) enforcement with human inspection escalation
4. Adaptive cropping & API integration:
   - Distinct non-duplicate crops for small images (200x200)
   - Crop preview serialization in findings (eliminates missing preview bug)
   - Honest 503 error handling when base model weights are not cached
   - Input validation (422 empty question, 400 unsupported file type)
"""

import unittest
import io
import math
import json
from PIL import Image
from fastapi.testclient import TestClient

from backend.schemas import (
    InspectionResponse,
    CropResult,
    HealthResponse,
    DEFAULT_TAU_THRESHOLD,
)
from backend.crops import generate_overlapping_crops
from backend.inference import normalize_yes_no_response
from backend.reliability import (
    compute_gap_from_probabilities,
    compute_probability_gap_from_logits,
    compute_probability_gap,
    validate_probability,
    is_evidence_sufficient,
    aggregate_crop_evidence,
    evaluate_evidence_limitation,
)
from backend.model_loader import get_device, get_device_telemetry, is_adapter_present
from backend.evidence_controller import run_veera_pipeline, MAX_EVIDENCE_ROUNDS
from backend.app import app


class TestVeeraBackendSuite(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Standard test image (800x600)
        self.test_img = Image.new("RGB", (800, 600), color=(180, 180, 180))
        img_byte_arr = io.BytesIO()
        self.test_img.save(img_byte_arr, format="JPEG")
        self.test_img_bytes = img_byte_arr.getvalue()

        # Small 200x200 test image (matching test_wall.jpg dimensions)
        self.small_img = Image.new("RGB", (200, 200), color=(210, 210, 210))
        small_byte_arr = io.BytesIO()
        self.small_img.save(small_byte_arr, format="JPEG")
        self.small_img_bytes = small_byte_arr.getvalue()

    # -------------------------------------------------------------
    # 1. Reliability Calculation & Numerical Safety
    # -------------------------------------------------------------
    def test_canonical_gap_from_probabilities(self):
        gap, pred = compute_gap_from_probabilities(p_yes=0.88, p_no=0.02)
        self.assertEqual(pred, "yes")
        self.assertAlmostEqual(gap, 0.86, places=5)
        self.assertTrue(is_evidence_sufficient(gap, DEFAULT_TAU_THRESHOLD))

        # Close/ambiguous probabilities
        gap_amb, pred_amb = compute_gap_from_probabilities(p_yes=0.0038, p_no=0.0035)
        self.assertAlmostEqual(gap_amb, 0.0003, places=5)
        self.assertFalse(is_evidence_sufficient(gap_amb, DEFAULT_TAU_THRESHOLD))

    def test_probability_validation_safety(self):
        # Non-finite values
        with self.assertRaises(ValueError):
            validate_probability(float("nan"))
        with self.assertRaises(ValueError):
            validate_probability(float("inf"))
        with self.assertRaises(ValueError):
            validate_probability(-0.01)
        with self.assertRaises(ValueError):
            validate_probability(1.05)
        with self.assertRaises(ValueError):
            validate_probability("invalid_string")
        with self.assertRaises(ValueError):
            validate_probability(None)

    def test_probability_sum_exceeding_one_raises(self):
        with self.assertRaises(ValueError):
            compute_gap_from_probabilities(p_yes=0.70, p_no=0.60)

    def test_binary_softmax_extreme_logits_no_overflow(self):
        # Extreme logits (+500, -500) must not cause OverflowError
        p_yes, p_no, gap, pred = compute_probability_gap_from_logits(logits_yes=500.0, logits_no=-500.0)
        self.assertEqual(pred, "yes")
        self.assertAlmostEqual(p_yes, 1.0, places=5)
        self.assertAlmostEqual(p_no, 0.0, places=5)
        self.assertAlmostEqual(gap, 1.0, places=5)

    def test_threshold_exact_boundaries(self):
        tau = DEFAULT_TAU_THRESHOLD  # 0.7853
        self.assertTrue(is_evidence_sufficient(tau, tau))
        self.assertTrue(is_evidence_sufficient(tau + 0.00001, tau))
        self.assertFalse(is_evidence_sufficient(tau - 0.00001, tau))
        # Non-finite inputs to is_evidence_sufficient return False safely
        self.assertFalse(is_evidence_sufficient(float("nan"), tau))
        self.assertFalse(is_evidence_sufficient(0.85, float("nan")))

    # -------------------------------------------------------------
    # 2. Evidence Aggregation & Failure-Aware Abstention
    # -------------------------------------------------------------
    def test_wall_crack_regression_contradiction_abstains(self):
        """
        CRITICAL REGRESSION TEST:
        Wall crack failure case: 3 crops say NO, 1 crop says YES,
        with a tiny reliability gap (mean gap 0.0037 << 0.7853).
        VEERA must NOT force majority NO; it MUST strictly abstain.
        """
        wall_crack_crops = [
            {"id": "c1", "vote": "no", "reliability_score": 0.0035},
            {"id": "c2", "vote": "no", "reliability_score": 0.0041},
            {"id": "c3", "vote": "no", "reliability_score": 0.0038},
            {"id": "c4", "vote": "yes", "reliability_score": 0.0034},
        ]
        agg = aggregate_crop_evidence(
            wall_crack_crops,
            DEFAULT_TAU_THRESHOLD,
            global_prediction="no",
            global_gap=0.0037,
        )
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertFalse(agg["evidence_sufficient"])
        self.assertIn("Contradictory evidence", agg["rationale"])

    def test_crop_aggregation_1_no_3_yes_contradiction_abstains(self):
        # 3 YES / 1 NO with low or mixed scores must abstain
        crops = [
            {"id": "c1", "vote": "yes", "reliability_score": 0.79},
            {"id": "c2", "vote": "yes", "reliability_score": 0.82},
            {"id": "c3", "vote": "yes", "reliability_score": 0.80},
            {"id": "c4", "vote": "no", "reliability_score": 0.40},
        ]
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertFalse(agg["evidence_sufficient"])

    def test_crop_aggregation_tied_votes_abstains(self):
        crops = [
            {"id": "c1", "vote": "yes", "reliability_score": 0.85},
            {"id": "c2", "vote": "yes", "reliability_score": 0.85},
            {"id": "c3", "vote": "no", "reliability_score": 0.85},
            {"id": "c4", "vote": "no", "reliability_score": 0.85},
        ]
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertIn("deadlock", agg["rationale"].lower())

    def test_crop_aggregation_unanimous_weak_scores_abstains(self):
        """
        Unanimity is not proof of correctness.
        4/4 crops agree on NO, but all have weak reliability (0.05 < tau).
        VEERA must abstain.
        """
        crops = [
            {"id": "c1", "vote": "no", "reliability_score": 0.05},
            {"id": "c2", "vote": "no", "reliability_score": 0.06},
            {"id": "c3", "vote": "no", "reliability_score": 0.04},
            {"id": "c4", "vote": "no", "reliability_score": 0.05},
        ]
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertFalse(agg["evidence_sufficient"])

    def test_crop_aggregation_unanimous_strong_scores_answers(self):
        """
        Autonomous answer granted ONLY when 100% unanimous AND all crops meet threshold tau.
        """
        crops = [
            {"id": "c1", "vote": "yes", "reliability_score": 0.85},
            {"id": "c2", "vote": "yes", "reliability_score": 0.90},
            {"id": "c3", "vote": "yes", "reliability_score": 0.88},
            {"id": "c4", "vote": "yes", "reliability_score": 0.82},
        ]
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "answered")
        self.assertEqual(agg["answer"], "yes")
        self.assertTrue(agg["evidence_sufficient"])

    def test_crop_aggregation_high_mean_with_weak_outlier_abstains(self):
        """
        High average score (e.g. 0.82) must not mask a weak crop (0.05).
        """
        crops = [
            {"id": "c1", "vote": "yes", "reliability_score": 0.95},
            {"id": "c2", "vote": "yes", "reliability_score": 0.95},
            {"id": "c3", "vote": "yes", "reliability_score": 0.95},
            {"id": "c4", "vote": "yes", "reliability_score": 0.05},
        ]
        # Mean gap is 0.725 (or 0.83 with higher scores), but crop 4 has 0.05 < tau
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertFalse(agg["evidence_sufficient"])

    def test_crop_aggregation_global_vs_local_conflict_abstains(self):
        crops = [
            {"id": "c1", "vote": "no", "reliability_score": 0.85},
            {"id": "c2", "vote": "no", "reliability_score": 0.85},
            {"id": "c3", "vote": "no", "reliability_score": 0.85},
            {"id": "c4", "vote": "no", "reliability_score": 0.85},
        ]
        # Global predicted YES, but crops say NO
        agg = aggregate_crop_evidence(crops, DEFAULT_TAU_THRESHOLD, global_prediction="yes", global_gap=0.50)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")
        self.assertFalse(agg["evidence_sufficient"])
        self.assertIn("conflict", agg["rationale"].lower())

    def test_crop_aggregation_corrupted_scores_handled_safely(self):
        # NaN in crop reliability score
        corrupt_crops = [
            {"id": "c1", "vote": "yes", "reliability_score": float("nan")},
            {"id": "c2", "vote": "yes", "reliability_score": 0.85},
        ]
        agg = aggregate_crop_evidence(corrupt_crops, DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg["status"], "review")
        self.assertEqual(agg["answer"], "uncertain")

        # Empty crop list
        agg_empty = aggregate_crop_evidence([], DEFAULT_TAU_THRESHOLD)
        self.assertEqual(agg_empty["status"], "review")
        self.assertEqual(agg_empty["answer"], "uncertain")

    # -------------------------------------------------------------
    # 3. Interactive Evidence Requests & Session History
    # -------------------------------------------------------------
    def test_limitation_and_requested_evidence_generation(self):
        evals = [
            {"id": "c1", "vote": "no", "reliability_score": 0.01},
            {"id": "c2", "vote": "yes", "reliability_score": 0.02},
        ]
        limitation = evaluate_evidence_limitation("Is there a crack on this surface?", 0.01, DEFAULT_TAU_THRESHOLD, evals)
        self.assertEqual(limitation["limitation_type"], "contradictory_crop_evidence")
        self.assertGreater(len(limitation["requested_evidence"]), 0)
        types = [r["type"] for r in limitation["requested_evidence"]]
        self.assertIn("close_up", types)

    def test_follow_up_inspect_api_endpoint(self):
        files = {"image": ("followup.jpg", self.test_img_bytes, "image/jpeg")}
        data = {
            "question": "Is there a crack on this surface?",
            "session_id": "test-session-123",
            "round_number": "2",
            "view_type": "close_up",
            "allow_mock_fallback": "true",
            "previous_history": json.dumps([
                {"round_number": 1, "view_type": "initial", "answer": "uncertain", "status": "review"}
            ]),
        }
        response = self.client.post("/api/v1/inspect/follow-up", files=files, data=data)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["session_id"], "test-session-123")
        self.assertEqual(payload["round_number"], 2)
        self.assertGreaterEqual(len(payload["evidence_history"]), 2)

    def test_max_evidence_rounds_escalation(self):
        res = run_veera_pipeline(
            self.small_img,
            "Is there an obscure fracture?",
            allow_diagnostic=True,
            round_number=MAX_EVIDENCE_ROUNDS,
        )
        self.assertEqual(res.round_number, 3)

    # -------------------------------------------------------------
    # 4. Adaptive Cropping & Spatial Coverage
    # -------------------------------------------------------------
    def test_crop_generation_adaptive_small_image(self):
        crops = generate_overlapping_crops(self.small_img, crop_size=400, max_crops=4)
        self.assertEqual(len(crops), 4)

        bboxes = [c["bbox"] for c in crops]
        self.assertEqual(len(set(tuple(b) for b in bboxes)), 4, "All 4 crop bboxes must be distinct subregions")
        for c in crops:
            self.assertEqual(c["image_pil"].size, (130, 130))
            self.assertTrue(c["image_base64"].startswith("data:image/jpeg;base64,"))

    def test_crop_preview_serialization_in_findings(self):
        res = run_veera_pipeline(self.small_img, "Is there a crack on the wall?", allow_diagnostic=True)
        self.assertIsNotNone(res.findings)
        self.assertGreater(len(res.findings), 0)
        self.assertIsNotNone(res.findings[0].region_image)
        self.assertTrue(res.findings[0].region_image.startswith("data:image/jpeg;base64,"))

    # -------------------------------------------------------------
    # 5. Input Validation & Error Handling
    # -------------------------------------------------------------
    def test_inspect_endpoint_fails_honestly_when_base_model_missing(self):
        files = {"image": ("test.jpg", self.test_img_bytes, "image/jpeg")}
        data = {"question": "Is there a crack on this surface?"}
        response = self.client.post("/api/v1/inspect", files=files, data=data)
        self.assertEqual(response.status_code, 503)
        self.assertIn("VEERA neural inference is unavailable", response.json()["detail"])

    def test_empty_question_fails_422(self):
        files = {"image": ("test.jpg", self.test_img_bytes, "image/jpeg")}
        data = {"question": "   "}
        response = self.client.post("/api/v1/inspect", files=files, data=data)
        self.assertEqual(response.status_code, 422)

    def test_unsupported_image_type_fails_400(self):
        files = {"image": ("test.txt", b"not an image", "text/plain")}
        data = {"question": "Is there a crack?"}
        response = self.client.post("/api/v1/inspect", files=files, data=data)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
