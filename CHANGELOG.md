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
| `main` | `43ac7e3` | ✅ | — (branche cible) |
| `feat/library-foundation` | `35de4b7` | ✅ origin | ✅ via PR #3 |
| `feat/ci-cd-quality` | `3cd29a9` | ✅ origin | ✅ via PR #3 |

> `feat/library-foundation` supprimée localement (contenu absorbé par PR #3).
> Prochaine branche prévue : `feat/multi-env-setup` (notebook externe Colab/ArcGIS — issue #1).

---

## [Non commité] — `main` · 2026-05-29

### Fixed
- `model.py` : `self.device` passe de `str` à `torch.device` — corrige l'erreur mypy
  détectée en CI (`_Wrapped.__call__` attendait `torch.device`, pas `str`).

### Changed
- `use_cases/pedestrian_crossing/notebook.ipynb` : ajustements du notebook de démo.

---

## `43ac7e3` — Merge PR #3 · `feat/ci-cd-quality` → `main` · 2026-05-29

### Added
- CI/CD GitHub Actions :
  - `.github/workflows/ci.yml` — `ruff` + `mypy` + `pytest` sur push/PR vers `main`.
  - `.github/workflows/release.yml` — sur tag `v*.*.*` : checks qualité, build de
    `geo_sam3_inference.zip` et création de la release GitHub avec le ZIP en asset.
- `.pre-commit-config.yaml` — hooks locaux `ruff` (lint + format) et `mypy`.
- `CHANGELOG.md` — historique du projet par branche avec statut de merge.
- Dépendances de dev : `ruff`, `mypy`, `pre-commit`.
- Dépendance de démo `ipywidgets` — supprime le `TqdmWarning` dans les notebooks.

### Changed
- Refonte du `README.md` : section utilisateur séparée d'une section contributeurs,
  avec diagrammes Mermaid du pipeline qualité et du flux de release.
- `pyproject.toml` : `filterwarnings` pytest pour masquer le `NotGeoreferencedWarning`.
- `model.py` : garde-fou étendu (`self.processor is None`).

### Removed
- `download_model()` — doublon de `from_pretrained`, jamais appelé.
- Dépendance `gradio` — aucun code associé dans le projet.
- Fichiers `tests/__init__.py` × 3 — vides et inutiles avec la config pytest.
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
