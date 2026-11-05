"""
VEERA — Pydantic Schemas for API Contracts

Aligned with VEERA.pdf and the structured response contract:
- Failure-aware disposition: "answered", "review", "insufficient_evidence"
- Categorical answer: "yes", "no", "uncertain"
- Reliability score: G(x, q) = |p_yes - p_no|
- Multi-crop visual evidence and spatial coordinates
- Evidence sufficiency gating and limitation explanation
- Interactive requested external visual evidence
- Inspection session history across evidence rounds
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

DEFAULT_TAU_THRESHOLD = 0.7853


class CropResult(BaseModel):
    id: str = Field(..., description="Unique crop identifier, e.g. crop_1")
    label: str = Field(..., description="Spatial label, e.g. Top-Left ROI or Center Region")
    bbox: List[int] = Field(..., description="Crop coordinates [ymin, xmin, ymax, xmax] in pixels")
    vote: str = Field(..., description="Local answer prediction: yes, no, or uncertain")
    reliability_score: float = Field(..., description="Local probability gap G(x_c, q)")
    notes: Optional[str] = Field(None, description="Diagnostic observation in this crop")
    image: Optional[str] = Field(None, description="Base64 encoded JPEG thumbnail of the crop")


class Finding(BaseModel):
    category: str = Field(..., description="Finding category, e.g. Crack, Damage, Surface Degradation")
    description: str = Field(..., description="Detailed description of the visual finding")
    evidence: str = Field(..., description="Visual evidence basis supporting this finding")
    region_image: Optional[str] = Field(None, description="Base64 crop thumbnail")


class VerificationInfo(BaseModel):
    performed: bool = Field(..., description="Whether adaptive verification was triggered")
    initial_assessment: Optional[str] = Field(None, description="Global full-image pass assessment")
    reassessment: Optional[str] = Field(None, description="Crop policy reassessment and vote outcome")
    additional_evidence_acquired: bool = Field(False, description="Whether crops were acquired and evaluated")


class RequestedEvidenceItem(BaseModel):
    type: str = Field(..., description="Requested view type: 'close_up', 'alternate_angle', 'wider_view'")
    instruction: str = Field(..., description="Specific photographic instruction for the user")
    rationale: Optional[str] = Field(None, description="Why this visual evidence is required")


class EvidenceSufficiency(BaseModel):
    sufficient: bool = Field(..., description="Whether evidence meets calibrated threshold and consistency")
    reason: str = Field(..., description="Explanation of sufficiency evaluation")
    limitation_type: Optional[str] = Field(None, description="Identified limitation: contradictory, blur, resolution")


class InspectionHistoryItem(BaseModel):
    round_number: int = Field(..., description="Sequential inspection round (1, 2, 3...)")
    view_type: str = Field(..., description="Type of image: 'initial', 'close_up', 'alternate_angle', etc.")
    answer: str = Field(..., description="Verdict in this round: yes, no, uncertain")
    reliability_score: float = Field(..., description="Reliability score in this round")
    status: str = Field(..., description="Disposition: answered, review, insufficient_evidence")
    reason: Optional[str] = Field(None, description="Summary rationale")


class InspectionResponse(BaseModel):
    # Core legacy fields for backward compatibility
    status: str = Field(..., description="'answered', 'review', or 'insufficient_evidence'")
    answer: str = Field(..., description="'yes', 'no', or 'uncertain'")
    reliability_score: float = Field(..., description="Calibrated empirical probability gap G(x, q)")
    evidence_inspections: int = Field(0, description="Count of additional crop inspections acquired")
    latency_seconds: float = Field(..., description="Total wall-clock inference latency in seconds")
    reason: str = Field(..., description="Diagnostic explanation synthesized from visual evidence")
    crops_inspected: List[CropResult] = Field(default_factory=list, description="Targeted crop evaluations")
    findings: List[Finding] = Field(default_factory=list, description="Structured visual findings")
    verification: Optional[VerificationInfo] = Field(None, description="Verification pipeline metadata")
    question: str = Field(..., description="The natural-language query evaluated")
    assessment: str = Field(..., description="High-level category: defect_detected, no_defect, inconclusive")
    summary: str = Field(..., description="Executive summary statement")
    device_used: Optional[str] = Field("cpu", description="Compute device: cuda, mps, or cpu")

    # Interactive evidence acquisition & explainability extensions
    initial_prediction: Optional[str] = Field(None, description="Initial global pass prediction")
    initial_gap: Optional[float] = Field(None, description="Initial global pass reliability gap")
    threshold: float = Field(DEFAULT_TAU_THRESHOLD, description="Validation threshold tau")
    additional_inspection_performed: bool = Field(False, description="Whether multi-crop inspection ran")
    evidence_sufficiency: Optional[EvidenceSufficiency] = Field(None, description="Sufficiency evaluation")
    requested_evidence: List[RequestedEvidenceItem] = Field(default_factory=list, description="Requested follow-up images")
    next_action: Optional[str] = Field(None, description="Recommended next action, e.g. 'upload_closer_image'")
    evidence_history: List[InspectionHistoryItem] = Field(default_factory=list, description="Audit trail of rounds")
    session_id: Optional[str] = Field(None, description="Unique inspection session ID")
    round_number: int = Field(1, description="Current inspection round number (1, 2, 3)")
    latency_breakdown: Optional[Dict[str, Optional[float]]] = Field(None, description="Stage-wise latency breakdown")


class HealthResponse(BaseModel):
    status: str = Field("ok", description="Service status ('ok' or 'model_weights_not_cached')")
    version: str = Field("1.0.0", description="VEERA API version")
    device: str = Field("cpu", description="Inference device: cuda, mps, cpu")
    base_model_id: str = Field("Qwen/Qwen2.5-VL-3B-Instruct", description="Base model name")
    lora_adapter_present: bool = Field(..., description="Whether VEERA LoRA weights are on disk")
    lora_adapter_loaded: bool = Field(False, description="Whether weights are loaded in memory")
    threshold_tau: float = Field(DEFAULT_TAU_THRESHOLD, description="Calibrated reliability threshold tau")
    device_details: Optional[Dict[str, Any]] = Field(None, description="Hardware compute specifications")
