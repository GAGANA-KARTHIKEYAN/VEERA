"""
VEERA — Model Loader & Singleton Manager

Manages safe loading and hardware allocation of:
- Base model: Qwen/Qwen2.5-VL-3B-Instruct
- Fine-tuned PEFT adapter: VEERA_finetuned_release/adapter/

Includes automatic hardware detection (CUDA / Apple Silicon MPS / CPU fallback),
precision selection, memory monitoring, and singleton caching.
"""

import os
from pathlib import Path
from typing import Optional, Tuple, Any, Dict

# Workspace paths
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ADAPTER_PATH = WORKSPACE_ROOT / "VEERA_finetuned_release" / "adapter"
BASE_MODEL_NAME = "Qwen/Qwen2.5-VL-3B-Instruct"

_model = None
_processor = None
_device = None


def get_adapter_path() -> Path:
    """Returns the adapter path, configurable via VEERA_ADAPTER_PATH env var."""
    custom_path = os.environ.get("VEERA_ADAPTER_PATH")
    if custom_path:
        return Path(custom_path)
    return DEFAULT_ADAPTER_PATH


def get_device() -> str:
    """
    Detects the best available hardware accelerator.
    Order of preference:
      1. CUDA (NVIDIA GPU with FP16/BF16 support)
      2. MPS (Apple Silicon Metal Performance Shaders)
      3. CPU (Functional fallback)
    """
    global _device
    if _device is not None:
        return _device

    try:
        import torch
        if torch.cuda.is_available():
            _device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            _device = "mps"
        else:
            _device = "cpu"
    except Exception:
        _device = "cpu"

    return _device


def get_device_telemetry() -> Dict[str, Any]:
    """Returns telemetry regarding available accelerator and memory."""
    device = get_device()
    info: Dict[str, Any] = {"device": device}
    try:
        import torch
        if device == "cuda" and torch.cuda.is_available():
            info["cuda_device_name"] = torch.cuda.get_device_name(0)
            info["cuda_device_count"] = torch.cuda.device_count()
            props = torch.cuda.get_device_properties(0)
            info["total_vram_gb"] = round(props.total_memory / (1024**3), 2)
            info["allocated_vram_mb"] = round(torch.cuda.memory_allocated(0) / (1024**2), 2)
            info["max_allocated_vram_mb"] = round(torch.cuda.max_memory_allocated(0) / (1024**2), 2)
        elif device == "mps":
            info["accelerator"] = "Apple Silicon MPS"
            info["recommended_dtype"] = "float32"
        else:
            info["accelerator"] = "CPU"
            info["recommended_dtype"] = "float32"
    except Exception as e:
        info["telemetry_error"] = str(e)
    return info


def is_adapter_present() -> bool:
    adapter_path = get_adapter_path()
    weights_path = adapter_path / "adapter_model.safetensors"
    config_path = adapter_path / "adapter_config.json"
    return weights_path.exists() and config_path.exists()


def is_base_model_cached() -> bool:
    """Check if Qwen2.5-VL-3B-Instruct base weights are present in HuggingFace cache."""
    hf_cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen2.5-VL-3B-Instruct"
    if not hf_cache.exists():
        return False
    snapshots = hf_cache / "snapshots"
    if snapshots.exists() and any(snapshots.iterdir()):
        return True
    return False


def set_loaded_model(model: Any, processor: Any):
    """
    Registers an already loaded model and processor into the singleton cache.
    Used by interactive deployment notebooks to prevent redundant reloading.
    """
    global _model, _processor
    _model = model
    _processor = processor


def load_model_and_processor():
    """
    Attempts to load the model and processor safely.
    Returns (model, processor, is_loaded_bool, error_message).
    """
    global _model, _processor
    if _model is not None and _processor is not None:
        return _model, _processor, True, None

    adapter_path = get_adapter_path()
    if not is_adapter_present():
        return None, None, False, f"LoRA adapter weights not found at {adapter_path}"

    device = get_device()
    allow_download = os.environ.get("VEERA_ALLOW_DOWNLOAD", "false").lower() in ("true", "1")

    # If base model is not cached and download is not permitted, return early
    if not is_base_model_cached() and not allow_download:
        return (
            None,
            None,
            False,
            f"Base model '{BASE_MODEL_NAME}' (~6.2 GB) not found in local cache (~/.cache/huggingface/hub). Standalone diagnostic engine active.",
        )

    try:
        import torch
        from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
        from peft import PeftModel

        local_only = not allow_download
        processor = AutoProcessor.from_pretrained(str(adapter_path), local_files_only=local_only)

        # Select compatible precision based on device
        if device == "cuda":
            model_dtype = torch.float16
        elif device == "mps":
            model_dtype = torch.float32
        else:
            model_dtype = torch.float32

        base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            BASE_MODEL_NAME,
            torch_dtype=model_dtype,
            device_map="auto" if device == "cuda" else None,
            local_files_only=local_only,
        )
        if device != "cuda":
            base_model = base_model.to(device)

        model = PeftModel.from_pretrained(base_model, str(adapter_path), local_files_only=local_only)
        model.eval()

        _model = model
        _processor = processor
        return _model, _processor, True, None

    except Exception as e:
        return None, None, False, f"Model loading error: {str(e)}"
