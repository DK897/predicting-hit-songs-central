# 🎵 Predicting Hit Songs Using Machine Learning

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)](https://scikit-learn.org/)
[![Accuracy](https://img.shields.io/badge/accuracy-79.8%25-brightgreen.svg)](#-model-performance)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Project Overview

This machine learning project predicts hit songs with **79.8% accuracy** by analyzing audio features from song choruses. The system identifies patterns in musical characteristics that contribute to commercial success, providing data-driven insights for the music industry.

**Course**: UE23CS352A Machine Learning  
**Institution**: PES University  
**Duration**: 2 Weeks (Sep 29 - Oct 13, 2025)

**Dataset Source**: [Kaggle - Spotify Hit Predictor Dataset](https://www.kaggle.com/datasets/theoverman/the-spotify-hit-predictor-dataset)

## 👥 Team Members

- **B. GOUTHAM** - PES1UG23CS132
- **DHARSHAN K** - PES1UG23CS184

## 🏆 Key Achievements

- **🎯 79.8% Accuracy** with Support Vector Machine
- **📊 41,106 Songs** across 6 decades (1960s-2010s)
- **🔧 66 Engineered Features** from audio characteristics
- **🤖 6 ML Models** comprehensively evaluated
- **📈 Business Insights** for music industry applications

## 🏗️ Project Structure

predicting-hit-songs-central/
├── 📁 data/ # Data storage
├── 📁 notebooks/ # Jupyter notebooks
├── 📁 src/ # Source code
│   ├── data/ # Data loading
│   ├── features/ # Feature engineering
│   ├── models/ # Model training
│   └── visualization/ # Plotting utilities
├── 📁 models/ # Trained models
├── 📁 reports/ # Reports & visualizations
├── 📁 tests/ # Unit tests
├── 📁 docs/ # Documentation
├── 📄 requirements.txt # Dependencies
└── 📄 README.md # This file


## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/your-username/predicting-hit-songs-central
cd predicting-hit-songs-central

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set Python path so `src` is importable
export PYTHONPATH="$PYTHONPATH:$(pwd)"
```

### Usage
Below are the most common commands. All scripts referenced exist in the repository root or the `scripts/` folder.

Run the full pipeline (data -> features -> train -> reports):

```bash
python src/main.py
```

Explore the data notebooks (run as scripts or open in Jupyter):

```bash
python notebooks/exploratory/01_data_exploration.py
python notebooks/modeling/02_model_training.py
```

Test trained models and produce sample predictions:

```bash
python scripts/test_trained_models.py
```

Notes:
- There is no top-level `predict_fixed.py` in the repository; prediction/testing utilities live under `scripts/` (e.g., `scripts/test_trained_models.py`).
- Trained models are expected under `models/saved_models/` (the repository includes several pre-saved models in that folder).

If you'd like a small demo prediction script at the repo root (for `python predict_fixed.py`), I can add one — say so and I'll create it.

