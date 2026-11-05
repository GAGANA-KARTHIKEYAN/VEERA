"""
VEERA — FastAPI Backend Application

Failure-Aware Visual Evidence Acquisition for Reliable Multimodal AI
Exposes:
- GET  /health                   : System, device, base model, LoRA status, and telemetry
- POST /api/v1/inspect           : Initial image inspection with failure-aware evidence acquisition
- POST /api/v1/inspect/follow-up : Interactive follow-up visual evidence acquisition
"""

import io
import json
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from .schemas import InspectionResponse, HealthResponse, DEFAULT_TAU_THRESHOLD
from .model_loader import (
    get_device,
    is_adapter_present,
    is_base_model_cached,
    BASE_MODEL_NAME,
    load_model_and_processor,
)
from .evidence_controller import run_veera_pipeline

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

app = FastAPI(
    title="VEERA Backend API",
    description="Failure-Aware Visual Evidence Acquisition and Adaptive Compute Allocation for Reliable Vision-Language Reasoning",
    version="1.1.0",
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Returns the operational health and readiness of the VEERA inference engine.
    Distinguishes server availability from neural model weight readiness.
    """
    device = get_device()
    adapter_ok = is_adapter_present()
    model, _, model_loaded, _ = load_model_and_processor()

    device_details: Dict[str, Any] = {"device": device}
    try:
        import torch
        if device == "cuda" and torch.cuda.is_available():
            device_details["device_name"] = torch.cuda.get_device_name(0)
            device_details["memory_allocated_mb"] = round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2)
            device_details["memory_reserved_mb"] = round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2)
        elif device == "mps":
            device_details["device_name"] = "Apple Silicon Metal Performance Shaders (MPS)"
    except Exception:
        pass

    return HealthResponse(
        status="ok" if model_loaded else "model_weights_not_cached",
        version="1.1.0",
        device=device,
        base_model_id=BASE_MODEL_NAME,
        lora_adapter_present=adapter_ok,
        lora_adapter_loaded=model_loaded,
        threshold_tau=DEFAULT_TAU_THRESHOLD,
        device_details=device_details,
    )


async def _parse_and_validate_image(image: UploadFile) -> Image.Image:
    """Helper to validate file size, content type, and PIL decode."""
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {image.content_type}. Supported: JPEG, PNG, WebP.",
        )

    file_bytes = await image.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of 10 MB ({len(file_bytes)} bytes).",
        )

    try:
        pil_image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        return pil_image
    except (UnidentifiedImageError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupted image file: {str(e)}",
        )


@app.post("/api/v1/inspect", response_model=InspectionResponse)
async def inspect_endpoint(
    image: UploadFile = File(..., description="Target image file (JPEG, PNG, WebP, max 10MB)"),
    question: str = Form(..., description="Natural-language inspection query"),
    threshold: Optional[float] = Form(DEFAULT_TAU_THRESHOLD, description="Calibrated tau threshold"),
    allow_mock_fallback: Optional[bool] = Form(False, description="For testing only; do not set in production"),
    session_id: Optional[str] = Form(None, description="Optional session identifier"),
    round_number: Optional[int] = Form(1, description="Sequential round number"),
    view_type: Optional[str] = Form("initial", description="Viewpoint classification"),
    previous_history: Optional[str] = Form(None, description="JSON string of previous inspection rounds"),
):
    """
    Inspects an image with failure-aware visual evidence acquisition.
    Rejects requests with 503 if the genuine base model weights are not loaded.
    """
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A non-empty natural-language inspection question is required.",
        )

    pil_image = await _parse_and_validate_image(image)

    # Check whether real model is loaded
    model, processor, model_loaded, load_err = load_model_and_processor()
    if not model_loaded and not allow_mock_fallback:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"VEERA neural inference is unavailable on this host: {load_err}. "
                f"Base weights for '{BASE_MODEL_NAME}' (~6.2 GB) must be loaded in a GPU-capable environment. "
                "The server will not fabricate or mock genuine model inferences."
            ),
        )

    parsed_history = None
    if previous_history:
        try:
            parsed_history = json.loads(previous_history)
        except Exception:
            parsed_history = None

    tau = threshold if (threshold is not None and 0.0 < threshold < 1.0) else DEFAULT_TAU_THRESHOLD
    result = run_veera_pipeline(
        pil_image,
        question=question.strip(),
        threshold=tau,
        allow_diagnostic=allow_mock_fallback,
        session_id=session_id,
        round_number=round_number or 1,
        view_type=view_type or "initial",
        previous_history=parsed_history,
    )
    return result


@app.post("/api/v1/inspect/follow-up", response_model=InspectionResponse)
async def follow_up_inspect_endpoint(
    image: UploadFile = File(..., description="Supplemental evidence image file"),
    question: str = Form(..., description="Original inspection query"),
    session_id: str = Form(..., description="Active inspection session ID"),
    round_number: int = Form(2, description="Iterative round number (2, 3...)"),
    view_type: str = Form("close_up", description="View type: 'close_up', 'alternate_angle', 'wider_view'"),
    threshold: Optional[float] = Form(DEFAULT_TAU_THRESHOLD, description="Calibrated tau threshold"),
    allow_mock_fallback: Optional[bool] = Form(False, description="For testing only"),
    previous_history: Optional[str] = Form(None, description="Serialized history of previous rounds"),
):
    """
    Processes additional visual evidence requested during an inconclusive inspection.
    Integrates new observations with the session history.
    """
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A non-empty natural-language inspection question is required.",
        )

    pil_image = await _parse_and_validate_image(image)

    model, processor, model_loaded, load_err = load_model_and_processor()
    if not model_loaded and not allow_mock_fallback:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"VEERA neural inference is unavailable on this host: {load_err}.",
        )

    parsed_history = None
    if previous_history:
        try:
            parsed_history = json.loads(previous_history)
        except Exception:
            parsed_history = None

    tau = threshold if (threshold is not None and 0.0 < threshold < 1.0) else DEFAULT_TAU_THRESHOLD
    result = run_veera_pipeline(
        pil_image,
        question=question.strip(),
        threshold=tau,
        allow_diagnostic=allow_mock_fallback,
        session_id=session_id,
        round_number=round_number,
        view_type=view_type,
        previous_history=parsed_history,
    )
    return result
