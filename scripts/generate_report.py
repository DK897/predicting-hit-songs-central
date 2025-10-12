"""
Generate a full evaluation report: metrics table, plots, and a markdown summary.

This script:
- Loads trained models from `models/saved_models/`.
- Loads processed test data using `DataLoader`.
- Applies `FeatureEngineer` to create features.
- Runs each model on the test set and computes metrics with `ModelEvaluator`.
- Saves a CSV (`reports/final_report/metrics_summary.csv`) and a markdown table
  (`reports/final_report/metrics_summary.md`) with the results.
- Calls existing Plotter/ModelEvaluator to create confusion matrices, ROC curves,
  feature importance and other visuals under `reports/figures/`.

Usage:
    python scripts/generate_report.py
    python scripts/generate_report.py --output-dir reports/final_report

"""

import argparse
from pathlib import Path
import pandas as pd
import joblib
import sys

# Make repo root importable
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.data.data_loader import DataLoader
from src.features.feature_engineer import FeatureEngineer
from src.models.model_evaluator import ModelEvaluator
from src.visualization.plotter import Plotter


def find_models(models_dir: Path):
    return sorted(models_dir.glob('*.pkl'))


def run_evaluation(models_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = Path('reports/figures')
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    loader = DataLoader()
    combined_df, train_df, test_df = loader.load_processed_data()

    # Prefer test_df if available
    if test_df is not None:
        data_df = test_df
    else:
        data_df = combined_df.sample(frac=0.25, random_state=42)

    fe = FeatureEngineer()
    features_df = fe.create_features(data_df)

    exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
    feature_columns = [c for c in features_df.columns if c not in exclude_cols]
    X_test = features_df[feature_columns]
    y_test = features_df['target']

    model_files = find_models(models_dir)
    if not model_files:
        print(f"No models found in {models_dir}")
        return

    evaluator = ModelEvaluator()
    plotter = Plotter()

    rows = []
    results = {}

    for model_file in model_files:
        name = model_file.stem
        print(f"Evaluating {name}...")
        try:
            model = joblib.load(model_file)
        except Exception as e:
            print(f"Failed to load {model_file}: {e}")
            continue

        # Handle scaling if necessary
        X_proc = X_test
        if any(k in name.lower() for k in ['svm', 'neural']):
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X_proc = scaler.fit_transform(X_test)

        try:
            y_pred = model.predict(X_proc)
            y_proba = model.predict_proba(X_proc)[:, 1] if hasattr(model, 'predict_proba') else None
        except Exception as e:
            print(f"Error predicting with {name}: {e}")
            continue

        metrics = evaluator.calculate_metrics(y_test, y_pred, y_proba)
        rows.append({
            'model': name,
            **metrics
        })

        # Save per-model results for plotting
        results[name] = {'model': model, 'y_pred': y_pred, 'y_proba': y_proba, 'accuracy': metrics.get('accuracy', 0.0), 'cv_mean': metrics.get('accuracy', 0.0)}

        # Save detailed visuals
        evaluator.generate_detailed_report(y_test, y_pred, y_proba, name)

    # Create summary table
    summary_df = pd.DataFrame(rows).sort_values('accuracy', ascending=False)
    csv_path = output_dir / 'metrics_summary.csv'
    md_path = output_dir / 'metrics_summary.md'
    summary_df.to_csv(csv_path, index=False)

    # Write markdown table
    with open(md_path, 'w') as f:
        f.write('# Metrics Summary\n\n')
        f.write(summary_df.to_markdown(index=False))
        f.write('\n')

    # Create comparative plots using plotter
    plotter.create_comprehensive_plots(features_df, results)

    # Create a small report file referencing outputs
    report_file = output_dir / 'report.md'
    with open(report_file, 'w') as f:
        f.write('# Evaluation Report\n\n')
        f.write('## Metrics Summary\n')
        f.write(f'- CSV: {csv_path}\n')
        f.write(f'- Markdown: {md_path}\n\n')
        f.write('## Figures\n')
        for p in sorted(figures_dir.glob('*.png')):
            f.write(f'- ![]({p.as_posix()})\n')

    print(f"Report generated under {output_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--models-dir', default='models/saved_models', help='Directory with saved models')
    parser.add_argument('--output-dir', default='reports/final_report', help='Directory to put summary and report')
    args = parser.parse_args()

    run_evaluation(Path(args.models_dir), Path(args.output_dir))


if __name__ == '__main__':
    main()
