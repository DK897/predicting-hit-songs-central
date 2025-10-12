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

def main():
    print("🎵 Hit Song Prediction Pipeline")
    print("=" * 50)
    
    try:
        # Initialize components
        data_loader = DataLoader()
        feature_engineer = FeatureEngineer()
        model_trainer = ModelTrainer()
        plotter = Plotter()
        
        # Step 1: Load and combine data
        print("\n📁 Step 1: Loading data...")
        df = data_loader.load_and_combine_data()
        
        # Step 2: Feature engineering
        print("\n🔧 Step 2: Feature engineering...")
        features_df = feature_engineer.create_features(df)
        
        # Step 3: Train models
        print("\n🤖 Step 3: Training models...")
        results = model_trainer.train_all_models(features_df)
        
        # Step 4: Generate reports
        print("\n📊 Step 4: Generating reports...")
        plotter.create_comprehensive_plots(features_df, results)
        
        print("\n🎉 Pipeline completed successfully!")
        print("Check reports/ directory for results and visualizations.")
        
    except Exception as e:
        print(f"❌ Error in pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()