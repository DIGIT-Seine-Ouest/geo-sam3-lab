import json
import logging
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import shapes
from PIL import Image

from .geo import GeoMetadata

logger = logging.getLogger(__name__)


def _merge_masks(masks: list[Image.Image], geo_meta: GeoMetadata) -> np.ndarray:
    merged = np.zeros((geo_meta.height, geo_meta.width), dtype=np.uint8)
    for mask in masks:
        merged = np.maximum(merged, np.array(mask))
    return merged


def export_geotiff(
    masks: list[Image.Image], geo_meta: GeoMetadata, path: str | Path
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = _merge_masks(masks, geo_meta)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=geo_meta.height,
        width=geo_meta.width,
        count=1,
        dtype=np.uint8,
        crs=geo_meta.crs,
        transform=geo_meta.transform,
    ) as dst:
        dst.write(merged, 1)
    logger.info("Exported GeoTIFF: %s", path)


def export_geojson(
    masks: list[Image.Image], geo_meta: GeoMetadata, path: str | Path
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = _merge_masks(masks, geo_meta)
    features = [
        {"type": "Feature", "geometry": geom, "properties": {"value": int(val)}}
        for geom, val in shapes(merged, transform=geo_meta.transform)
        if val > 0
    ]
    geojson = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(geojson, indent=2))
    logger.info("Exported GeoJSON: %s (%d features)", path, len(features))
