"""
Model Training Notebook
Training and evaluating machine learning models for hit song prediction.
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# Fix import path - add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.data.data_loader import DataLoader
from src.features.feature_engineer import FeatureEngineer
from src.models.model_trainer import ModelTrainer
from src.models.model_evaluator import ModelEvaluator
from src.visualization.plotter import Plotter

def main():
    print("🤖 Model Training Pipeline")
    print("=" * 40)
    
    # Load data using the updated DataLoader
    loader = DataLoader()
    combined_df, train_df, test_df = loader.load_processed_data()
    
    # If we have separate train/test, use them. Otherwise, split combined data
    if train_df is not None and test_df is not None:
        print("Using pre-split train/test datasets")
        # Feature engineering on both sets
        feature_engineer = FeatureEngineer()
        
        # Fit on train, transform both
        train_features = feature_engineer.create_features(train_df)
        test_features = feature_engineer.create_features(test_df)
        
        # Combine for model training (we'll handle split in model_trainer)
        features_df = pd.concat([train_features, test_features], ignore_index=True)
        # We'll need to track which rows are train vs test
        train_indices = range(len(train_features))
        test_indices = range(len(train_features), len(features_df))
        
    else:
        print("Splitting combined dataset into train/test")
        # Feature engineering on combined data
        feature_engineer = FeatureEngineer()
        features_df = feature_engineer.create_features(combined_df)
        train_indices = None
        test_indices = None
    
    # Model training
    trainer = ModelTrainer()
    
    # Pass indices if we have pre-split data
    if train_indices is not None and test_indices is not None:
        results = trainer.train_all_models(features_df, train_indices, test_indices)
    else:
        results = trainer.train_all_models(features_df)
    
    # Evaluation
    evaluator = ModelEvaluator()
    
    print(f"\n🏆 Model Results:")
    for model_name, result in results.items():
        print(f"{model_name}: Accuracy = {result['accuracy']:.3f}")
    
    # Visualizations
    plotter = Plotter()
    plotter.create_comprehensive_plots(features_df, results)
    
    # Get best model
    best_model_name, best_result = trainer.get_best_model()
    print(f"\n🎯 Best Model: {best_model_name} (Accuracy: {best_result['accuracy']:.3f})")
    
    print(f"\n✅ Model training completed!")

if __name__ == "__main__":
    main()