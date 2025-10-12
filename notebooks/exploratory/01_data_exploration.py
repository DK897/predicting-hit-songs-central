"""
Data Exploration Notebook
Comprehensive exploratory data analysis for hit song prediction.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from pathlib import Path

# Fix import path - add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.data.data_loader import DataLoader
from src.visualization.plotter import Plotter

def main():
    print("🔍 Exploratory Data Analysis")
    print("=" * 40)
    
    # Load data using the updated DataLoader
    loader = DataLoader()
    combined_df, train_df, test_df = loader.load_processed_data()
    
    print(f"📊 Dataset Information:")
    print(f"Total songs: {len(combined_df)}")
    if train_df is not None and test_df is not None:
        print(f"Training set: {len(train_df)} songs")
        print(f"Test set: {len(test_df)} songs")
    
    print(f"Features: {len(combined_df.columns)}")
    print(f"Columns: {combined_df.columns.tolist()}")
    
    # Basic info
    print(f"\n🎯 Target Analysis:")
    target_counts = combined_df['target'].value_counts()
    print(f"Hit songs: {target_counts.get(1, 0)} ({target_counts.get(1, 0)/len(combined_df)*100:.1f}%)")
    print(f"Non-hit songs: {target_counts.get(0, 0)} ({target_counts.get(0, 0)/len(combined_df)*100:.1f}%)")
    
    # Decade distribution
    if 'decade' in combined_df.columns:
        print(f"\n📅 Decade Distribution:")
        decade_counts = combined_df['decade'].value_counts().sort_index()
        for decade, count in decade_counts.items():
            hit_rate = combined_df[combined_df['decade'] == decade]['target'].mean() * 100
            print(f"  {decade}: {count} songs, Hit rate: {hit_rate:.1f}%")
    
    # Audio features summary
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness', 'tempo']
    
    available_audio = [f for f in audio_features if f in combined_df.columns]
    
    if available_audio:
        print(f"\n🎧 Audio Features Summary (Hit vs Non-Hit):")
        for feature in available_audio:
            hit_mean = combined_df[combined_df['target'] == 1][feature].mean()
            non_hit_mean = combined_df[combined_df['target'] == 0][feature].mean()
            print(f"  {feature}: Hit={hit_mean:.3f}, Non-hit={non_hit_mean:.3f}")
    
    # Create visualizations
    plotter = Plotter()
    plotter.plot_target_distribution(combined_df)
    plotter.plot_feature_correlations(combined_df)
    
    print(f"\n✅ EDA completed! Check reports/figures/ for visualizations.")

if __name__ == "__main__":
    main()