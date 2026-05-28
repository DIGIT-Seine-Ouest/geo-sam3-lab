import numpy as np
import pytest
import rasterio
from affine import Affine

from geo_sam3_inference.validate import InvalidGeoTIFFError, validate_geotiff


def test_valid(sample_geotiff):
    validate_geotiff(sample_geotiff)


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_geotiff(tmp_path / "missing.tif")


def test_wrong_extension(tmp_path):
    f = tmp_path / "img.png"
    f.write_bytes(b"fake")
    with pytest.raises(InvalidGeoTIFFError):
        validate_geotiff(f)


def test_no_crs(tmp_path):
    path = tmp_path / "nocrs.tif"
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=512,
        width=512,
        count=1,
        dtype=np.uint8,
    ) as dst:
        dst.write(np.zeros((1, 512, 512), dtype=np.uint8))
    with pytest.raises(InvalidGeoTIFFError):
        validate_geotiff(path)


def test_wrong_tile_size_warns(tmp_path):
    path = tmp_path / "big.tif"
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=1024,
        width=1024,
        count=1,
        dtype=np.uint8,
        crs="EPSG:2154",
        transform=Affine(0.2, 0, 0, 0, -0.2, 0),
    ) as dst:
        dst.write(np.zeros((1, 1024, 1024), dtype=np.uint8))
    # should not raise, only warn
    validate_geotiff(path)
