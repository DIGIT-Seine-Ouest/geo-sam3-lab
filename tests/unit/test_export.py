import json

import rasterio

from geo_sam3_inference.export import export_geojson, export_geotiff


def test_export_geotiff_creates_file(sample_mask, sample_geo_meta, tmp_path):
    out = tmp_path / "out.tif"
    export_geotiff([sample_mask], sample_geo_meta, out)
    assert out.exists()


def test_export_geotiff_preserves_crs(sample_mask, sample_geo_meta, tmp_path):
    out = tmp_path / "out.tif"
    export_geotiff([sample_mask], sample_geo_meta, out)
    with rasterio.open(out) as src:
        assert src.crs == sample_geo_meta.crs
        assert src.width == 512
        assert src.height == 512


def test_export_geojson_creates_file(sample_mask, sample_geo_meta, tmp_path):
    out = tmp_path / "out.geojson"
    export_geojson([sample_mask], sample_geo_meta, out)
    assert out.exists()


def test_export_geojson_valid_structure(sample_mask, sample_geo_meta, tmp_path):
    out = tmp_path / "out.geojson"
    export_geojson([sample_mask], sample_geo_meta, out)
    data = json.loads(out.read_text())
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0
