"""
Main pipeline for Hit Song Prediction Project
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_loader import DataLoader
from src.features.feature_engineer import FeatureEngineer
from src.models.model_trainer import ModelTrainer
from src.visualization.plotter import Plotter

# Optional import for report generation (script provides run_evaluation)
try:
    from scripts.generate_report import run_evaluation
except Exception:
    run_evaluation = None

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Run full hit-song prediction pipeline')
    parser.add_argument('--no-report', action='store_true', help='Skip report generation step')
    parser.add_argument('--models-dir', default='models/saved_models', help='Directory containing saved models')
    parser.add_argument('--report-out', default='reports/final_report', help='Output directory for generated report')
    args = parser.parse_args()

    logger.info("🎵 Hit Song Prediction Pipeline")
    logger.info("Starting pipeline...")

    # Initialize components
    data_loader = DataLoader()
    feature_engineer = FeatureEngineer()
    model_trainer = ModelTrainer()
    plotter = Plotter()

    try:
        # Step 1: Load processed data (train/test) if available
        logger.info("📁 Step 1: Loading processed data (or raw files)...")
        combined_df, train_df, test_df = data_loader.load_processed_data()

        # Use combined dataset for feature engineering and training
        df = combined_df

        # Step 2: Feature engineering
        logger.info("🔧 Step 2: Feature engineering...")
        features_df = feature_engineer.create_features(df)

        # Step 3: Train models
        logger.info("🤖 Step 3: Training models...")
        results = model_trainer.train_all_models(features_df)

        # Step 4: Generate visualizations
        logger.info("📊 Step 4: Generating visualizations...")
        try:
            plotter.create_comprehensive_plots(features_df, results)
        except Exception as e:
            logger.exception("Error while creating visualizations: %s", e)

        # Step 5: Generate report (optional)
        if not args.no_report:
            logger.info("📑 Step 5: Generating final report...")
            if run_evaluation is not None:
                try:
                    run_evaluation(Path(args.models_dir), Path(args.report_out))
                except Exception as e:
                    logger.exception("Report generation failed: %s", e)
            else:
                # Fallback: call the script as a subprocess
                import subprocess
                try:
                    subprocess.run([sys.executable, 'scripts/generate_report.py', '--models-dir', args.models_dir, '--output-dir', args.report_out], check=True)
                except Exception as e:
                    logger.exception("Report generation via subprocess failed: %s", e)

        logger.info("🎉 Pipeline completed successfully!")
        logger.info("Check reports/ directory for results and visualizations.")

    except Exception as e:
        logger.exception("❌ Error in pipeline: %s", e)

if __name__ == "__main__":
    main()