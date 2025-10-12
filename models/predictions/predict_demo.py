"""
Simple demo prediction script.
- Loads the first available model from `models/saved_models/` (*.pkl)
- Accepts an optional input CSV path (features or raw) and creates features using `FeatureEngineer`
- Writes predictions to `models/predictions/predictions_demo.csv`

Usage:
    python models/predictions/predict_demo.py [--input path/to/songs.csv] [--model models/saved_models/svm.pkl]

If no input is provided, two sample songs are used.
"""

import argparse
import sys
from pathlib import Path
import joblib
import pandas as pd

# Add project root to path so we can import src modules
# File is at models/predictions/, so parents[2] points to the repository root
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.features.feature_engineer import FeatureEngineer


def find_first_model(models_dir: Path):
    # Prefer a file named 'themodel.pkl' if present (user requested), then 'svm.pkl',
    # otherwise return the first available .pkl
    preferred = models_dir / "themodel.pkl"
    if preferred.exists():
        return preferred
    svm = models_dir / "svm.pkl"
    if svm.exists():
        return svm
    models = list(models_dir.glob("*.pkl"))
    return models[0] if models else None


def load_model(path: Path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Error loading model {path}: {e}")
        return None


def prepare_input(input_path: Path):
    # If input CSV provided, load it. Otherwise, create sample songs.
    if input_path and input_path.exists():
        df = pd.read_csv(input_path)
        print(f"Loaded input data: {input_path} ({len(df)} rows)")
    else:
        print("No input CSV provided or file not found — using sample songs.")
        sample_songs = [
            {
                'danceability': 0.8, 'energy': 0.9, 'loudness': -5.0,
                'speechiness': 0.05, 'acousticness': 0.1, 'instrumentalness': 0.0,
                'liveness': 0.2, 'valence': 0.9, 'tempo': 120, 'duration_ms': 200000,
                'chorus_hit': 45.2, 'sections': 4, 'decade': '10s'
            },
            {
                'danceability': 0.3, 'energy': 0.4, 'loudness': -15.0,
                'speechiness': 0.8, 'acousticness': 0.9, 'instrumentalness': 0.1,
                'liveness': 0.1, 'valence': 0.3, 'tempo': 80, 'duration_ms': 300000,
                'chorus_hit': 20.1, 'sections': 6, 'decade': '10s'
            }
        ]
        df = pd.DataFrame(sample_songs)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Path to input CSV with song rows (optional)")
    parser.add_argument("--model", help="Path to model .pkl to use (optional)")
    args = parser.parse_args()

    models_dir = Path(repo_root) / "models" / "saved_models"
    output_dir = Path(repo_root) / "models" / "predictions"
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = Path(args.model) if args.model else None
    if not model_path:
        first = find_first_model(models_dir)
        if not first:
            print(f"No models found in {models_dir}. Please train or add a model first.")
            return
        model_path = first

    model = load_model(model_path)
    if model is None:
        return

    # Prepare input
    input_path = Path(args.input) if args.input else None
    raw_df = prepare_input(input_path)

    # Feature engineering
    fe = FeatureEngineer()
    features_df = fe.create_features(raw_df)

    # Decide feature columns (exclude non-feature cols)
    exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
    feature_columns = [c for c in features_df.columns if c not in exclude_cols]
    X = features_df[feature_columns]

    # If model needs scaling or special handling, try to detect
    try:
        if any(k in model.__class__.__name__.lower() for k in ['svc', 'svm', 'neural']):
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_proc = scaler.fit_transform(X)
        else:
            X_proc = X
    except Exception:
        X_proc = X

    # Predict
    try:
        preds = model.predict(X_proc)
        probs = model.predict_proba(X_proc)[:, 1] if hasattr(model, 'predict_proba') else [None] * len(preds)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return

    results = features_df.copy()
    results['prediction'] = preds
    results['probability'] = probs

    output_file = output_dir / 'predictions_demo.csv'
    results.to_csv(output_file, index=False)
    print(f"Predictions saved to: {output_file}")


if __name__ == '__main__':
    main()
