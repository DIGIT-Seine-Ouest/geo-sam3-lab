import numpy as np
from PIL import Image

from geo_sam3_inference.export import export_geotiff
from geo_sam3_inference.geo import GeoImageReader
from geo_sam3_inference.validate import validate_geotiff


def test_full_pipeline(sample_geotiff, tmp_path):
    validate_geotiff(sample_geotiff)

    image, geo_meta = GeoImageReader.read(sample_geotiff)
    assert image.size == (512, 512)

    # modèle mocké : on simule un masque retourné par SAM3
    mask = Image.fromarray(np.zeros((512, 512), dtype=np.uint8))
    masks = [mask]

    out = tmp_path / "result.tif"
    export_geotiff(masks, geo_meta, out)
    assert out.exists()
