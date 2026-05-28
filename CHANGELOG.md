# Changelog

Toutes les évolutions notables du projet sont documentées ici.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et le projet suit le [versionnage sémantique](https://semver.org/lang/fr/).

> Aucune version n'a encore été taguée. Tant qu'aucun tag `v*.*.*` n'est poussé,
> tout le contenu ci-dessous est en cours et n'a pas fait l'objet d'une release.

---

## Statut des branches

| Branche | Dernier commit | Poussée | Mergée dans `main` |
|---|---|---|---|
| `main` | `1d6f6b5` | ✅ | — (branche cible) |
| `feat/library-foundation` | `35de4b7` | ✅ origin | ❌ non |
| `feat/ci-cd-quality` | *(non commité)* | ❌ | ❌ non |

> `feat/ci-cd-quality` (ex-`feat/multi-env-setup`, renommée) est créée à partir de
> `feat/library-foundation` : elle contient déjà `5de0e8a` + `35de4b7`. La merger dans
> `main` amène donc à la fois la fondation et l'outillage. Le notebook multi-env
> (Colab/ArcGIS) reste à venir dans une future branche `feat/multi-env-setup`.

---

## [Non commité] — branche `feat/ci-cd-quality` · 2026-05-29

Travaux de qualité, d'outillage et de nettoyage. **Pas encore commité ni poussé.**

### Added
- CI/CD GitHub Actions :
  - `.github/workflows/ci.yml` — `ruff` + `mypy` + `pytest` sur push/PR vers `main`.
  - `.github/workflows/release.yml` — sur tag `v*.*.*` : checks qualité, build de
    `geo_sam3_inference.zip` et création de la release GitHub avec le ZIP en asset.
- `.pre-commit-config.yaml` — hooks locaux `ruff` (lint + format) et `mypy`.
- `CHANGELOG.md` — historique du projet par branche avec statut de merge.
- Dépendances de dev : `ruff`, `mypy`, `pre-commit`.
- Dépendance de démo `ipywidgets` — supprime le `TqdmWarning` (IProgress) des
  barres de progression dans les notebooks.

### Changed
- Refonte du `README.md` : section utilisateur (fonctionnement → utilisation →
  use cases) séparée d'une section contributeurs (structure → outillage → releases),
  avec diagrammes Mermaid du pipeline qualité et du flux de release.
- `pyproject.toml` : `filterwarnings` pytest pour masquer le
  `NotGeoreferencedWarning` de rasterio (attendu sur les fixtures sans CRS).
- `model.py` : garde-fou étendu (`self.processor is None`) pour la cohérence du typage.

### Removed
- `download_model()` (et son export) — doublon de `from_pretrained`, jamais appelé.
- Dépendance `gradio` — aucun code associé dans le projet.
- Fichiers `tests/__init__.py`, `tests/unit/__init__.py`,
  `tests/functional/__init__.py` — vides et inutiles avec la config pytest.
- Fixture `sample_geo_meta` non utilisée dans `test_pipeline.py`.

---

## [feat/library-foundation] — poussée, non mergée

### `35de4b7` — Première inférence de la librairie · 2026-05-29

#### Added
- Inférence SAM3 réelle dans `Sam3InferenceEngine.predict_masks`
  (chargement modèle/processor, post-traitement des masques).
- Sélection automatique du device : `cuda` → `mps` (Apple Silicon) → `cpu`.
- Dépendance `accelerate`.
- Démo interactive complète dans `use_cases/pedestrian_crossing/notebook.ipynb`
  (validation → lecture → inférence → visualisation → export).

### `5de0e8a` — Architecture de base du projet · 2026-05-28

#### Added
- Librairie `geo_sam3_inference/` :
  - `validate.py` — validation stricte des GeoTIFF (format, CRS, taille 512).
  - `geo.py` — `GeoImageReader` + `GeoMetadata`.
  - `model.py` — squelette `Sam3InferenceEngine`.
  - `visualize.py` — `draw_overlay`, `draw_contours`, `compute_stats`.
  - `export.py` — `export_geotiff`, `export_geojson`.
  - `download.py` — login HuggingFace.
  - `__init__.py` — API publique + logging `NullHandler`.
- Suite de tests `pytest` : unitaires (validate, geo, visualize, export) +
  fonctionnel (pipeline complet, modèle mocké), avec fixtures partagées.
- Packaging `pyproject.toml` (hatchling), extras `dev` et `demo`.
- `use_cases/pedestrian_crossing/` : README, notebook, images de démo.
- `.env.example`, `.gitignore`, `LICENSE` (MIT).

---

## [main] — publié

### `1d6f6b5` — Titre et description · 2026-05-28

#### Added
- Titre et description du projet dans le `README.md`.
