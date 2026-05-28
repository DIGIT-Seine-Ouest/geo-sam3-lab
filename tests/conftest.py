import numpy as np
import pytest
import rasterio
from affine import Affine
from PIL import Image
from rasterio.crs import CRS

from geo_sam3_inference.geo import GeoMetadata


@pytest.fixture
def sample_geotiff(tmp_path):
    path = tmp_path / "test.tif"
    transform = Affine(0.2, 0, 700000, 0, -0.2, 6600000)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=512,
        width=512,
        count=3,
        dtype=np.uint8,
        crs=CRS.from_epsg(2154),
        transform=transform,
    ) as dst:
        dst.write(np.random.randint(0, 255, (3, 512, 512), dtype=np.uint8))
    return path


@pytest.fixture
def sample_mask():
    data = np.zeros((512, 512), dtype=np.uint8)
    data[100:200, 100:200] = 255
    return Image.fromarray(data)


@pytest.fixture
def sample_geo_meta():
    return GeoMetadata(
        crs=CRS.from_epsg(2154),
        transform=Affine(0.2, 0, 700000, 0, -0.2, 6600000),
        width=512,
        height=512,
    )
