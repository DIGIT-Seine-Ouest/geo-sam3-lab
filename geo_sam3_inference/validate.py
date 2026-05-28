import logging
from pathlib import Path

import rasterio

logger = logging.getLogger(__name__)

EXPECTED_TILE_SIZE = 512


class InvalidGeoTIFFError(Exception):
    pass


def validate_geotiff(path: str | Path) -> None:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() not in (".tif", ".tiff"):
        raise InvalidGeoTIFFError(f"{path.name} is not a .tif file")

    with rasterio.open(path) as src:
        if src.crs is None:
            raise InvalidGeoTIFFError(f"{path.name} has no CRS")

        if src.width != EXPECTED_TILE_SIZE or src.height != EXPECTED_TILE_SIZE:
            logger.warning(
                "%s: expected %dx%d, got %dx%d (run gdal_retile first)",
                path.name,
                EXPECTED_TILE_SIZE,
                EXPECTED_TILE_SIZE,
                src.width,
                src.height,
            )

    logger.debug("Valid GeoTIFF: %s", path)
