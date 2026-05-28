import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class GeoMetadata:
    crs: object
    transform: object
    width: int
    height: int


class GeoImageReader:
    @staticmethod
    def read(path: str | Path) -> tuple[Image.Image, GeoMetadata]:
        with rasterio.open(path) as src:
            data = src.read()
            meta = GeoMetadata(
                crs=src.crs,
                transform=src.transform,
                width=src.width,
                height=src.height,
            )

        if data.shape[0] >= 3:
            rgb = np.moveaxis(data[:3], 0, -1)
        else:
            rgb = np.stack([data[0]] * 3, axis=-1)

        image = Image.fromarray(rgb.astype(np.uint8))
        logger.debug("Read %s: %dx%d CRS=%s", path, meta.width, meta.height, meta.crs)
        return image, meta
