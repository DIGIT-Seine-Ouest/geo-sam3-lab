# Use case — Détection de passages piétons

Segmentation zero-shot de passages piétons (zebra crossing) sur orthophoto IGN 2024.

---

## Flux de prédiction

```mermaid
flowchart TD
    A[GeoTIFF ortho / satellite] --> B[validate.py\nformat GeoTIFF ?\nCRS présent ?]
    B -->|invalide| ERR[Exception\narret]
    B -->|valide| C[geo.py\nGeoImageReader.read\nPIL Image + GeoMetadata]
    C --> D[model.py\nSam3InferenceEngine\npredict_masks\nprompt · threshold]
    D --> E{Masques détectés ?}
    E -->|non| EMPTY[Résultat vide\naucun passage trouvé]
    E -->|oui| F[visualize.py\noverlay + contours\nstats count · coverage]
    F --> G[export.py]
    G --> G1[GeoTIFF raster\nbinaire géoréférencé]
    G --> G2[GeoJSON vectoriel\npolygones par instance]
```

---

## Lancer

```bash
jupyter lab notebook.ipynb
```

---

## Sorties

```
output/
├── pedestrian_crossings.tif      # raster binaire géoréférencé (EPSG:2154)
├── pedestrian_crossings.geojson  # polygones vectoriels par instance
└── visualization.png             # overlay pour vérification visuelle
```

Le GeoTIFF exporté conserve exactement le CRS et la transform de l'image d'entrée — il s'ouvre directement dans QGIS superposé à l'ortho source.

---

## Résultats attendus

| Métrique | Valeur typique |
|---|---|
| Passages détectés par tuile | 0 à 3 |
| Couverture moyenne | 2 à 8% |
| Faux positifs fréquents | Marquages au sol, bandes de stationnement |

Les faux positifs diminuent en abaissant `THRESHOLD` (défaut `0.35`) ou en affinant le prompt (`"zebra crossing"` plutôt que `"pedestrian crossing"`).

---

## Librairie utilisée

[geo_sam3_inference/](../../geo_sam3_inference/)
