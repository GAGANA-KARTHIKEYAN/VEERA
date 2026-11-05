"""
VEERA — Failure-Aware Visual Evidence Controller

Orchestrates the entire VEERA workflow:
1. Global initial pass on (image, question) using Qwen2.5-VL-3B-Instruct + LoRA adapter.
2. Evaluation of canonical empirical reliability signal G(x, q) = |p_Yes - p_No|.
3. Calibration gate against validation threshold tau = 0.7853.
4. If G(x, q) < tau:
     - Multi-crop targeted evidence acquisition (adaptive regions).
     - Local crop voting & probability gap assessment.
     - Contradiction detection & evidence sufficiency evaluation.
5. Explicit Abstention decision if evidence remains contradictory or below threshold:
     - Identifies root cause of limitation (blur, low resolution, contradictions).
     - Generates tailored requested evidence (close-up, oblique angle, wider context).
6. Multi-round evidence session tracking across follow-up uploads.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from PIL import Image

from .schemas import (
    InspectionResponse,
    CropResult,
    Finding,
    VerificationInfo,
    RequestedEvidenceItem,
    EvidenceSufficiency,
    InspectionHistoryItem,
    DEFAULT_TAU_THRESHOLD,
)
from .reliability import (
    compute_gap_from_probabilities,
    is_evidence_sufficient,
    aggregate_crop_evidence,
    evaluate_evidence_limitation,
)
from .crops import generate_overlapping_crops
from .model_loader import get_device, load_model_and_processor
from .inference import run_qwen_inference

MAX_EVIDENCE_ROUNDS = 3


def run_veera_pipeline(
    image: Image.Image,
    question: str,
    threshold: float = DEFAULT_TAU_THRESHOLD,
    allow_diagnostic: bool = False,
    session_id: Optional[str] = None,
    round_number: int = 1,
    view_type: str = "initial",
    previous_history: Optional[List[Dict[str, Any]]] = None,
) -> InspectionResponse:
    """
    Executes the VEERA inspection pipeline for a given image and natural-language question.
    Supports single-shot and multi-round iterative evidence acquisition.
    """
    overall_start = time.perf_counter()
    device = get_device()
    model, processor, model_loaded, load_err = load_model_and_processor()

    clean_question = question.strip()
    if not clean_question:
        clean_question = "Is there a defect on this surface?"

    current_session_id = session_id or str(uuid.uuid4())[:8]
    history: List[InspectionHistoryItem] = []
    if previous_history:
        for item in previous_history:
            history.append(
                InspectionHistoryItem(
                    round_number=item.get("round_number", 1),
                    view_type=item.get("view_type", "initial"),
                    answer=item.get("answer", "uncertain"),
                    reliability_score=item.get("reliability_score", 0.0),
                    status=item.get("status", "review"),
                    reason=item.get("reason"),
                )
            )

    # -------------------------------------------------------------
    # Case A: Live Fine-tuned Model is Loaded in Memory
    # -------------------------------------------------------------
    if model_loaded and model is not None and processor is not None:
        # 1. Global Pass Inference
        t_global_0 = time.perf_counter()
        global_inf = run_qwen_inference(model, processor, image, clean_question, device=device)
        global_latency = round(time.perf_counter() - t_global_0, 3)
        global_gap = global_inf["reliability_gap"]
        initial_ans = global_inf["normalized_answer"]

        # Check if global evidence alone is sufficient
        if is_evidence_sufficient(global_gap, threshold):
            total_elapsed = round(time.perf_counter() - overall_start, 3)

            history.append(
                InspectionHistoryItem(
                    round_number=round_number,
                    view_type=view_type,
                    answer=initial_ans,
                    reliability_score=global_gap,
                    status="answered",
                    reason=f"Global inspection confident (G={global_gap:.2%} >= tau={threshold:.2%}).",
                )
            )

            return InspectionResponse(
                status="answered",
                answer=initial_ans,
                reliability_score=global_gap,
                evidence_inspections=0,
                latency_seconds=total_elapsed,
                reason=(
                    f"Initial global inspection was confident with canonical reliability gap "
                    f"G(x, q) = {global_gap:.2%} exceeding validation threshold tau = {threshold:.2%}."
                ),
                crops_inspected=[],
                findings=[
                    Finding(
                        category="Autonomous Pass",
                        description=f"Global image analysis resolved query with answer: {initial_ans.upper()}.",
                        evidence=f"p(Yes)={global_inf['p_yes']:.3f}, p(No)={global_inf['p_no']:.3f}, gap={global_gap:.3f}",
                    )
                ],
                verification=VerificationInfo(
                    performed=False,
                    initial_assessment=f"Sufficient certainty ({global_gap:.2%}). Direct answer: {initial_ans.upper()}.",
                    additional_evidence_acquired=False,
                ),
                question=clean_question,
                assessment="defect_detected" if initial_ans == "yes" else "no_defect",
                summary=f"Analysis completed autonomously with high reliability ({global_gap:.2%}).",
                device_used=device,
                initial_prediction=initial_ans,
                initial_gap=global_gap,
                threshold=threshold,
                additional_inspection_performed=False,
                evidence_sufficiency=EvidenceSufficiency(
                    sufficient=True,
                    reason=f"Reliability gap ({global_gap:.2%}) meets threshold tau ({threshold:.2%}).",
                ),
                requested_evidence=[],
                next_action=None,
                evidence_history=history,
                session_id=current_session_id,
                round_number=round_number,
                latency_breakdown={
                    "initial_inference_seconds": global_latency,
                    "crop_inspection_seconds": 0.0,
                    "total_seconds": total_elapsed,
                },
            )

        # 2. Global pass insufficient (G < tau) -> Trigger Adaptive Crop Verification
        t_crop_0 = time.perf_counter()
        raw_crops = generate_overlapping_crops(image)
        crop_results: List[CropResult] = []
        crop_eval_dicts: List[Dict[str, Any]] = []

        for crop_data in raw_crops:
            c_img = crop_data["image_pil"]
            c_inf = run_qwen_inference(model, processor, c_img, clean_question, device=device)

            crop_res = CropResult(
                id=crop_data["id"],
                label=crop_data["label"],
                bbox=crop_data["bbox"],
                vote=c_inf["normalized_answer"],
                reliability_score=c_inf["reliability_gap"],
                notes=f"Local gap G={c_inf['reliability_gap']:.2%}, vote={c_inf['normalized_answer'].upper()}",
                image=crop_data["image_base64"],
            )
            crop_results.append(crop_res)
            crop_eval_dicts.append({
                "id": crop_data["id"],
                "vote": c_inf["normalized_answer"],
                "reliability_score": c_inf["reliability_gap"],
            })

        crop_latency = round(time.perf_counter() - t_crop_0, 3)

        # 3. Aggregate multi-crop evidence with failure-aware abstention safeguards
        agg = aggregate_crop_evidence(
            crop_evaluations=crop_eval_dicts,
            threshold=threshold,
            global_prediction=initial_ans,
            global_gap=global_gap,
        )
        total_elapsed = round(time.perf_counter() - overall_start, 3)

        # 4. Determine evidence limitation and tailor follow-up requests if inconclusive
        limitation_info = evaluate_evidence_limitation(
            question=clean_question,
            global_gap=global_gap,
            threshold=threshold,
            crop_evaluations=crop_eval_dicts,
            image_size=image.size,
        )

        is_insufficient = (agg["status"] == "review" or not agg["evidence_sufficient"])

        # Enforce max evidence rounds guard
        next_action = None
        requested_items: List[RequestedEvidenceItem] = []
        if is_insufficient:
            if round_number >= MAX_EVIDENCE_ROUNDS:
                next_action = "recommend_human_inspection"
                agg["rationale"] += (
                    f" Maximum iterative evidence rounds ({MAX_EVIDENCE_ROUNDS}) reached without resolving ambiguity. "
                    "Recommend on-site physical inspection by a qualified expert."
                )
            else:
                next_action = "upload_additional_evidence"
                requested_items = [
                    RequestedEvidenceItem(
                        type=req["type"],
                        instruction=req["instruction"],
                        rationale=req["rationale"],
                    )
                    for req in limitation_info["requested_evidence"]
                ]

        # Fix missing crop preview: ensure finding carries the primary ROI thumbnail
        primary_roi_image = crop_results[0].image if crop_results else None
        findings = [
            Finding(
                category="Multi-Crop Verification [Failure-Aware Policy]",
                description=agg["rationale"],
                evidence=(
                    f"Inspected {len(crop_results)} localized crops. Consensus ratio: {agg['consensus_ratio']:.0%}, "
                    f"mean crop gap: {agg['mean_gap']:.2%}."
                ),
                region_image=primary_roi_image,
            )
        ]

        history.append(
            InspectionHistoryItem(
                round_number=round_number,
                view_type=view_type,
                answer=agg["answer"],
                reliability_score=agg["mean_gap"],
                status=agg["status"],
                reason=agg["rationale"],
            )
        )

        return InspectionResponse(
            status=agg["status"],
            answer=agg["answer"],
            reliability_score=agg["mean_gap"],
            evidence_inspections=len(crop_results),
            latency_seconds=total_elapsed,
            reason=agg["rationale"],
            crops_inspected=crop_results,
            findings=findings,
            verification=VerificationInfo(
                performed=True,
                initial_assessment=f"Initial global pass was ambiguous (G={global_gap:.2%} < tau={threshold:.2%}).",
                reassessment=agg["rationale"],
                additional_evidence_acquired=True,
            ),
            question=clean_question,
            assessment="inconclusive" if agg["status"] == "review" else ("defect_detected" if agg["answer"] == "yes" else "no_defect"),
            summary=(
                "Abstention Policy Triggered: Inconclusive Evidence."
                if is_insufficient
                else f"Adaptive Verification Succeeded: {agg['answer'].upper()}."
            ),
            device_used=device,
            initial_prediction=initial_ans,
            initial_gap=global_gap,
            threshold=threshold,
            additional_inspection_performed=True,
            evidence_sufficiency=EvidenceSufficiency(
                sufficient=not is_insufficient,
                reason=limitation_info["reason"] if is_insufficient else "Multi-crop evidence satisfied consensus and threshold criteria.",
                limitation_type=limitation_info["limitation_type"] if is_insufficient else None,
            ),
            requested_evidence=requested_items,
            next_action=next_action,
            evidence_history=history,
            session_id=current_session_id,
            round_number=round_number,
            latency_breakdown={
                "initial_inference_seconds": global_latency,
                "crop_inspection_seconds": crop_latency,
                "total_seconds": total_elapsed,
            },
        )

    # -------------------------------------------------------------
    # Case B: Offline Diagnostic Simulation (Testing Only)
    # -------------------------------------------------------------
    if not allow_diagnostic:
        raise RuntimeError(f"Base model is not loaded ({load_err}). Genuine inference requires model weights.")

    t_crop_0 = time.perf_counter()
    raw_crops = generate_overlapping_crops(image)
    is_crack_query = any(k in clean_question.lower() for k in ["crack", "fracture", "break", "damage", "scratch"])

    crop_results: List[CropResult] = []
    crop_eval_dicts: List[Dict[str, Any]] = []
    for c in raw_crops:
        gray = c["image_pil"].convert("L")
        stat = gray.getextrema()
        contrast = (stat[1] - stat[0]) / 255.0
        c_vote = "yes" if contrast > 0.45 and is_crack_query else ("no" if contrast < 0.25 else "uncertain")
        c_gap = round(0.79 + (contrast * 0.15), 4) if c_vote != "uncertain" else 0.42

        crop_res = CropResult(
            id=c["id"],
            label=c["label"],
            bbox=c["bbox"],
            vote=c_vote if c_vote != "uncertain" else "yes",
            reliability_score=c_gap,
            notes=f"Diagnostic simulation (contrast: {contrast:.2f})",
            image=c["image_base64"],
        )
        crop_results.append(crop_res)
        crop_eval_dicts.append({"id": c["id"], "vote": crop_res.vote, "reliability_score": c_gap})

    crop_latency = round(time.perf_counter() - t_crop_0, 3)
    agg = aggregate_crop_evidence(
        crop_evaluations=crop_eval_dicts,
        threshold=threshold,
        global_prediction="no",
        global_gap=0.35,
    )
    total_elapsed = round(time.perf_counter() - overall_start, 3)

    limitation_info = evaluate_evidence_limitation(
        question=clean_question,
        global_gap=0.35,
        threshold=threshold,
        crop_evaluations=crop_eval_dicts,
        image_size=image.size,
    )

    is_insufficient = (agg["status"] == "review" or not agg["evidence_sufficient"])
    next_action = "upload_additional_evidence" if is_insufficient else None
    requested_items = [
        RequestedEvidenceItem(
            type=req["type"],
            instruction=req["instruction"],
            rationale=req["rationale"],
        )
        for req in limitation_info["requested_evidence"]
    ] if is_insufficient else []

    primary_roi_image = crop_results[0].image if crop_results else None
    findings = [
        Finding(
            category="Offline Test Simulation",
            description=agg["rationale"],
            evidence="Offline unit test fixture.",
            region_image=primary_roi_image,
        )
    ]

    history.append(
        InspectionHistoryItem(
            round_number=round_number,
            view_type=view_type,
            answer=agg["answer"],
            reliability_score=agg["mean_gap"],
            status=agg["status"],
            reason=agg["rationale"],
        )
    )

    return InspectionResponse(
        status=agg["status"],
        answer=agg["answer"],
        reliability_score=agg["mean_gap"],
        evidence_inspections=len(crop_results),
        latency_seconds=total_elapsed,
        reason=agg["rationale"] + " [Offline Test Harness Simulation Only]",
        crops_inspected=crop_results,
        findings=findings,
        verification=VerificationInfo(
            performed=True,
            initial_assessment="Offline test simulation.",
            reassessment=agg["rationale"],
            additional_evidence_acquired=True,
        ),
        question=clean_question,
        assessment="inconclusive" if agg["status"] == "review" else ("defect_detected" if agg["answer"] == "yes" else "no_defect"),
        summary=f"Simulation complete: {agg['status'].upper()}",
        device_used=device,
        initial_prediction="no",
        initial_gap=0.35,
        threshold=threshold,
        additional_inspection_performed=True,
        evidence_sufficiency=EvidenceSufficiency(
            sufficient=not is_insufficient,
            reason=limitation_info["reason"] if is_insufficient else "Crop agreement satisfied test threshold.",
            limitation_type=limitation_info["limitation_type"] if is_insufficient else None,
        ),
        requested_evidence=requested_items,
        next_action=next_action,
        evidence_history=history,
        session_id=current_session_id,
        round_number=round_number,
        latency_breakdown={
            "initial_inference_seconds": 0.05,
            "crop_inspection_seconds": crop_latency,
            "total_seconds": total_elapsed,
        },
    )
