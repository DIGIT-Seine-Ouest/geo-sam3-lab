from PIL import Image

from geo_sam3_inference.geo import GeoImageReader, GeoMetadata


def test_read_returns_image_and_meta(sample_geotiff):
    image, meta = GeoImageReader.read(sample_geotiff)
    assert isinstance(image, Image.Image)
    assert image.size == (512, 512)
    assert image.mode == "RGB"
    assert isinstance(meta, GeoMetadata)
    assert meta.crs is not None
    assert meta.width == 512
    assert meta.height == 512
