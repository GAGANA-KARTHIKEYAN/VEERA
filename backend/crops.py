"""
VEERA — Image Cropping & Adaptive Region Acquisition Module

Replicates and refines the multi-crop extraction logic established in
updated-till-26oct-veera-research-pipeline-v1.ipynb:
- Extracts overlapping crops focused on key spatial regions
- Adapts crop size proportionally for small or irregular aspect-ratio images (prevents duplicate full-image crops)
- Calculates relative bounding boxes [ymin, xmin, ymax, xmax] in pixels
- Encodes crops as base64 JPEG strings for frontend UI inspection and evidence traceability
"""

import io
import base64
from typing import List, Tuple, Dict, Any
from PIL import Image


def generate_overlapping_crops(
    image: Image.Image,
    crop_size: int = 400,
    stride_ratio: float = 0.5,
    max_crops: int = 4,
) -> List[Dict[str, Any]]:
    """
    Generate distinct overlapping crops of the input image.

    Adaptive Behavior:
    - If image dimensions W, H are smaller than or equal to crop_size (e.g. 200x200):
      Scales crop window to 65% of (W, H) so that distinct quadrants/center are examined
      rather than returning 4 identical copies of the full image.
    - Handles arbitrary aspect ratios (e.g. wide panoramas, tall vertical images).
    - Ensures every crop has a distinct non-degenerate bounding box.

    Returns:
        List of dicts containing:
            - id: crop identifier (crop_1, crop_2, ...)
            - label: positional description
            - bbox: [ymin, xmin, ymax, xmax] in pixels
            - image_pil: cropped PIL Image
            - image_base64: data URI formatted base64 string
    """
    if image is None:
        raise ValueError("Cannot crop None image.")

    w, h = image.size
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid image dimensions: ({w}, {h}).")

    # Proportionally adapt crop size if the input is smaller than crop_size
    if w <= crop_size or h <= crop_size:
        actual_crop_w = max(16, int(w * 0.65))
        actual_crop_h = max(16, int(h * 0.65))
    else:
        actual_crop_w = min(crop_size, w)
        actual_crop_h = min(crop_size, h)

    # Ensure crop size is strictly within bounds
    actual_crop_w = max(1, min(actual_crop_w, w))
    actual_crop_h = max(1, min(actual_crop_h, h))

    crops = []
    crop_idx = 1

    # Define 4 distinct spatial regions covering quadrants and center
    center_x = max(0, (w - actual_crop_w) // 2)
    center_y = max(0, (h - actual_crop_h) // 2)

    positions = [
        ("Top-Left Region", (0, 0, actual_crop_w, actual_crop_h)),
        ("Center ROI", (center_x, center_y, center_x + actual_crop_w, center_y + actual_crop_h)),
        ("Top-Right Region", (max(0, w - actual_crop_w), 0, w, actual_crop_h)),
        ("Bottom-Right Region", (max(0, w - actual_crop_w), max(0, h - actual_crop_h), w, h)),
    ]

    seen_bboxes = set()

    for label, (left, top, right, bottom) in positions:
        if len(crops) >= max_crops:
            break

        left_cl = max(0, min(int(left), w - 1))
        top_cl = max(0, min(int(top), h - 1))
        right_cl = max(left_cl + 1, min(int(right), w))
        bottom_cl = max(top_cl + 1, min(int(bottom), h))

        bbox_tuple = (top_cl, left_cl, bottom_cl, right_cl)
        # Avoid duplicate crops if image is extremely small (e.g. 20x20)
        if bbox_tuple in seen_bboxes and len(crops) > 0:
            continue
        seen_bboxes.add(bbox_tuple)

        crop_img = image.crop((left_cl, top_cl, right_cl, bottom_cl))

        # Encode thumbnail to base64
        thumb = crop_img.copy()
        thumb.thumbnail((240, 240))
        buffer = io.BytesIO()
        thumb.save(buffer, format="JPEG", quality=80)
        b64_str = f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

        crops.append({
            "id": f"crop_{crop_idx}",
            "label": label,
            "bbox": [top_cl, left_cl, bottom_cl, right_cl],
            "image_pil": crop_img,
            "image_base64": b64_str,
        })
        crop_idx += 1

    return crops
