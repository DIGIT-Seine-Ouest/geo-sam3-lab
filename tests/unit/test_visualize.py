import numpy as np
from PIL import Image

from geo_sam3_inference.visualize import compute_stats, draw_contours, draw_overlay


def test_draw_overlay(sample_mask):
    image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
    result = draw_overlay(image, [sample_mask], (255, 0, 0), 0.5)
    assert result.size == (512, 512)
    assert result.mode == "RGB"


def test_draw_contours(sample_mask):
    image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
    result = draw_contours(image, [sample_mask])
    assert result.size == (512, 512)


def test_compute_stats(sample_mask):
    image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
    stats = compute_stats([sample_mask], image)
    assert stats["count"] == 1
    assert stats["coverage_pct"] > 0
    assert len(stats["areas"]) == 1


def test_compute_stats_no_masks():
    image = Image.fromarray(np.zeros((512, 512, 3), dtype=np.uint8))
    stats = compute_stats([], image)
    assert stats["count"] == 0
    assert stats["coverage_pct"] == 0.0
