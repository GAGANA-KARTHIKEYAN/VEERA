"""
VEERA — Neural Inference Module

Faithfully implements the inference procedure from the research notebook
(updated-till-26oct-veera-research-pipeline-v1.ipynb, Cells 9, 15, 291, 335, and 339):
1. Format conversational message with chat template:
   messages = [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": f"{question} Answer with only yes or no."}]}]
2. Process vision info with qwen_vl_utils.process_vision_info to extract image tensors.
3. Generate next-token logits and decode raw answer.
4. Extract softmax probabilities for primary tokens:
   - Token "Yes": token ID 9454 under Qwen2.5-VL tokenizer
   - Token "No" : token ID 2753 under Qwen2.5-VL tokenizer
5. Compute empirical reliability gap G(x, q) = |p_Yes - p_No|.
6. Normalize answer string to 'yes', 'no', or 'unclear'.
"""

import time
from typing import Tuple, Dict, Any, Optional
from PIL import Image

try:
    import torch
    import torch.nn.functional as F
except ImportError:
    torch = None
    F = None

try:
    from qwen_vl_utils import process_vision_info
except ImportError:
    process_vision_info = None

# Qwen2.5-VL verified token IDs for post-newline answer generation
TOKEN_ID_YES = 9454  # 'Yes'
TOKEN_ID_NO = 2753   # 'No'


def normalize_yes_no_response(text: str) -> str:
    """
    Directly matches veera_normalize_answer from notebook Cell 335.
    """
    clean = text.strip().lower()
    first = clean.split()[0].strip(".,!?;:") if clean else ""
    if first in {"yes", "no"}:
        return first
    if "yes" in clean and "no" not in clean:
        return "yes"
    if "no" in clean and "yes" not in clean:
        return "no"
    return "unclear"


def run_qwen_inference(
    model: Any,
    processor: Any,
    image: Image.Image,
    question: str,
    device: str = "cpu",
) -> Dict[str, Any]:
    """
    Executes single-pass vision-language inference faithful to notebook Cell 335, 15 & 9.

    Returns dict containing:
        - raw_response: decoded generation text
        - normalized_answer: 'yes' | 'no' | 'unclear'
        - p_yes: float probability of 'Yes' token (ID 9454)
        - p_no: float probability of 'No' token (ID 2753)
        - reliability_gap: float |p_yes - p_no|
        - latency_seconds: execution time
    """
    if torch is None or model is None or processor is None:
        raise RuntimeError("PyTorch or model/processor is not initialized.")

    start_time = time.perf_counter()

    # Match notebook prompt phrasing (Cell 9 & 335)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image.convert("RGB")},
                {
                    "type": "text",
                    "text": f"{question} Answer with only yes or no.",
                },
            ],
        }
    ]

    # Apply chat template and extract vision inputs
    prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    if process_vision_info is not None:
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[prompt],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
    else:
        # Fallback if qwen_vl_utils is not present
        inputs = processor(
            text=[prompt],
            images=[image.convert("RGB")],
            padding=True,
            return_tensors="pt",
        )

    # Move tensors to model device
    target_device = next(model.parameters()).device if hasattr(model, "parameters") else device
    inputs = {
        k: v.to(target_device)
        for k, v in inputs.items()
        if isinstance(v, torch.Tensor)
    }

    # 1. Forward pass to extract next-token logits for Yes/No (Cell 15 & 291)
    with torch.inference_mode():
        outputs = model(**inputs)
        # Last prompt token position predicts the first answer token
        next_token_logits = outputs.logits[0, -1].float()
        # Softmax over full vocabulary as in Cell 15 & 291
        probs = F.softmax(next_token_logits, dim=-1)

        # 2. Generate answer tokens (notebook generates max 5 tokens, do_sample=False)
        generated = model.generate(
            **inputs,
            max_new_tokens=5,
            do_sample=False,
        )

    prompt_length = inputs["input_ids"].shape[1]
    output_ids = generated[:, prompt_length:]
    raw_response = processor.batch_decode(
        output_ids,
        skip_special_tokens=True,
    )[0].strip()

    # Resolve token IDs dynamically or fall back to verified constants
    tokenizer = getattr(processor, "tokenizer", None)
    if tokenizer is not None:
        yes_enc = tokenizer.encode("Yes", add_special_tokens=False)
        no_enc = tokenizer.encode("No", add_special_tokens=False)
        yes_id = yes_enc[0] if yes_enc else TOKEN_ID_YES
        no_id = no_enc[0] if no_enc else TOKEN_ID_NO
    else:
        yes_id = TOKEN_ID_YES
        no_id = TOKEN_ID_NO

    p_yes = float(probs[yes_id].item())
    p_no = float(probs[no_id].item())

    # Empirical probability gap G(x, q) = |p_Yes - p_No|
    reliability_gap = abs(p_yes - p_no)
    normalized_answer = normalize_yes_no_response(raw_response)

    # If normalized is unclear, fallback to argmax of probabilities
    if normalized_answer not in {"yes", "no"}:
        normalized_answer = "yes" if p_yes >= p_no else "no"

    elapsed = time.perf_counter() - start_time

    return {
        "raw_response": raw_response,
        "normalized_answer": normalized_answer,
        "p_yes": round(p_yes, 4),
        "p_no": round(p_no, 4),
        "yes_token_id": yes_id,
        "no_token_id": no_id,
        "reliability_gap": round(reliability_gap, 4),
        "latency_seconds": round(elapsed, 3),
    }
