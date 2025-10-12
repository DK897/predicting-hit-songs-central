# 🎵 Predicting Hit Songs Using Machine Learning

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)](https://scikit-learn.org/)
[![Accuracy](https://img.shields.io/badge/accuracy-79.8%25-brightgreen.svg)](#-model-performance)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A compact, reproducible repository for predicting whether a song will be a commercial "hit" using audio features extracted from choruses. The project includes feature engineering, model training for several algorithms, evaluation utilities, visualizations, and demo scripts.

Key facts
- Course: UE23CS352A Machine Learning (PES University)
- Dataset: Spotify Hit Predictor (Kaggle)
- Notable result: 79.8% accuracy (SVM reported in experiments)

Table of contents
- Project layout
- Installation
- Quick usage
- Data, features, and configuration
- Models and demos
- Reproducing experiments
- Troubleshooting

Project layout (top-level)

predicting-hit-songs-central/
├── data/ (raw, external, processed)
├── notebooks/ (exploratory and modeling notebooks)
├── src/ (source code: data, features, models, visualization)
├── models/
│   ├── saved_models/ (pretrained .pkl models)
│   └── predictions/ (prediction outputs, demo script)
├── reports/ (figures and final report)
├── scripts/ (utility scripts used in demos and submission)
├── requirements.txt
├── config/config.yaml
└── README.md


Installation

1. Clone and create a virtual environment

```bash
git clone https://github.com/DK897/predicting-hit-songs-central.git
cd predicting-hit-songs-central
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. (Optional) Make the `src` package importable from scripts

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```


Quick usage

- Run the full pipeline (load, feature-engineer, train, visualize):

```bash
python src/main.py
```

- Run model evaluation and sample predictions (script):

```bash
python scripts/test_trained_models.py
```

- Demo: run a lightweight prediction on a CSV or sample songs (writes CSV to `models/predictions/`):

```bash
# auto-selects models/saved_models/themodel.pkl -> svm.pkl -> first .pkl
python models/predictions/predict_demo.py --input data/processed/test_dataset.csv

# or explicitly pick a model
python models/predictions/predict_demo.py --model models/saved_models/svm.pkl --input data/processed/test_dataset.csv
```


Data, features, and configuration

- Data layout is defined under `data/`. Processed CSVs used for training/testing live in `data/processed/` (e.g. `train_dataset.csv`, `test_dataset.csv`).
- Feature engineering is implemented in `src/features/feature_engineer.py`. The active audio features and excluded columns are defined in `config/config.yaml`.

Key config excerpts (see `config/config.yaml`):

```yaml
data:
	raw_path: "data/raw"
	processed_path: "data/processed"

features:
	audio_features:
		- danceability
		- energy
		- valence
		- acousticness
		- instrumentalness
		- liveness
		- speechiness
		- tempo

models:
	svm:
		probability: true
		random_state: 42
	random_forest:
		n_estimators: 100
```


Models and demos

- Pretrained models (for demo and evaluation) are in `models/saved_models/` and include:
	- `svm.pkl`, `random_forest.pkl`, `xgboost.pkl`, `neural_network.pkl`, `gradient_boosting.pkl`, `logistic_regression.pkl`
- Demo script: `models/predictions/predict_demo.py` — small CLI that loads a model, runs feature engineering (via `FeatureEngineer`), and writes predictions to `models/predictions/predictions_demo.csv`.
- Evaluation script: `scripts/test_trained_models.py` — loads all saved models, runs them on the test split, prints metrics, and generates diagnostic figures under `reports/figures/`.


Reproducing experiments

1. Prepare data
	 - Put raw CSVs into `data/raw/` and processed CSVs under `data/processed/`.
	 - If you have the original Kaggle dataset, place it under `data/raw/` and run the preprocessing steps in `src/data/data_loader.py` or use the notebooks.

2. Run the pipeline

```bash
python src/main.py
```

3. Validate models & view reports

```bash
python scripts/test_trained_models.py
# check reports/figures/ for confusion matrices, ROC curves, feature importance
```


Troubleshooting & notes

- If `ModuleNotFoundError: No module named 'src'` appears when running scripts directly, set PYTHONPATH as above or run scripts through the package entrypoints (e.g., `python -m src.main` after setting PYTHONPATH or installing the package).
- `predict_demo.py` searches for `models/saved_models/themodel.pkl` first, then `svm.pkl`, then the first `.pkl` found.
- Large model files (e.g. `random_forest.pkl`, `neural_network.pkl`) are included under `models/saved_models/` and may increase repo size.


Development and testing

- Unit tests live under `tests/`. Run the basic tests with:

```bash
pytest -q
```

Contact & license

- Authors: B. GOUTHAM (PES1UG23CS132) and DHARSHAN K (PES1UG23CS184)
- License: MIT (see `LICENSE`)


If you'd like, I can:
- Add a short `CONTRIBUTING.md` and `USAGE.md` for students and reviewers.
- Create an installable package (setup.py is present) so you can `pip install -e .` and run entrypoints.
- Add a small top-level `predict_fixed.py` CLI wrapper that calls `models/predictions/predict_demo.py` for even simpler demos.

----

Quick verification (what I checked while writing this README):
- `requirements.txt`, `config/config.yaml`, `src/main.py`, `scripts/test_trained_models.py`, and `models/predictions/predict_demo.py`.



