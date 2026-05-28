import logging

import numpy as np
from PIL import Image, ImageFilter

logger = logging.getLogger(__name__)


def draw_overlay(
    image: Image.Image,
    masks: list[Image.Image],
    color: tuple[int, int, int],
    opacity: float,
) -> Image.Image:
    result = image.copy().convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    r, g, b = color
    alpha = int(opacity * 255)
    for mask in masks:
        fill = Image.new("RGBA", image.size, (r, g, b, alpha))
        overlay.paste(fill, mask=mask)
    return Image.alpha_composite(result, overlay).convert("RGB")


def draw_contours(
    image: Image.Image,
    masks: list[Image.Image],
    color: tuple[int, int, int] = (255, 50, 0),
) -> Image.Image:
    result = image.copy()
    for mask in masks:
        eroded = mask.filter(ImageFilter.MinFilter(5))
        contour = np.clip(
            np.array(mask).astype(int) - np.array(eroded).astype(int), 0, 255
        ).astype(np.uint8)
        color_layer = Image.new("RGB", image.size, color)
        result.paste(color_layer, mask=Image.fromarray(contour))
    return result


def compute_stats(masks: list[Image.Image], image: Image.Image) -> dict:
    w, h = image.size
    covered = np.zeros((h, w), dtype=bool)
    areas = []
    for mask in masks:
        mask_np = np.array(mask) > 127
        areas.append(int(mask_np.sum()))
        covered |= mask_np
    return {
        "count": len(masks),
        "areas": areas,
        "coverage_pct": round(100.0 * covered.sum() / (w * h), 2),
    }
