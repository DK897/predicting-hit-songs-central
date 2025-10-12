# Final Evaluation Report

This folder contains the generated evaluation artifacts produced by `scripts/generate_report.py`:

- `metrics_summary.csv` — CSV table with per-model metrics (accuracy, precision, recall, f1, roc_auc where available).
- `metrics_summary.md` — A markdown table version of the metrics for quick viewing.
- `report.md` — A simple report that references the generated figures and tables.
- `figures/` — Visualizations produced during evaluation are saved under `reports/figures/` (confusion matrices, ROC curves, feature importances, model comparison, etc.).

Run the generator with:

```bash
python scripts/generate_report.py --models-dir models/saved_models --output-dir reports/final_report
```

Open `reports/final_report/report.md` to view a simple layout with figures embedded.
