"""
Visualization utilities for hit song prediction.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Plotter:
    def __init__(self):
        self.figures_path = Path("reports/figures")
        self.figures_path.mkdir(parents=True, exist_ok=True)
        plt.style.use('seaborn-v0_8')
        
    def plot_target_distribution(self, df):
        """Plot distribution of target variable."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Count plot
        target_counts = df['target'].value_counts()
        ax1.bar(['Non-Hit (0)', 'Hit (1)'], target_counts.values, color=['skyblue', 'lightcoral'])
        ax1.set_title('Distribution of Hit vs Non-Hit Songs')
        ax1.set_ylabel('Count')
        
        # Add percentage labels
        total = len(df)
        for i, count in enumerate(target_counts.values):
            ax1.text(i, count + 5, f'{count/total*100:.1f}%', ha='center')
        
        # Decade-wise hit rate
        if 'decade' in df.columns:
            hit_rates = df.groupby('decade')['target'].mean().sort_index()
            ax2.bar(hit_rates.index, hit_rates.values, color='lightgreen')
            ax2.set_title('Hit Rate by Decade')
            ax2.set_ylabel('Hit Rate')
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'target_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("Saved target distribution plot")
    
    def plot_feature_correlations(self, df):
        """Plot correlation matrix of features."""
        # Select only numerical columns for correlation
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numerical_cols].corr()
        
        # Plot top correlations with target
        if 'target' in corr_matrix.columns:
            target_correlations = corr_matrix['target'].drop('target').sort_values(ascending=False)
            
            plt.figure(figsize=(10, 8))
            top_features = target_correlations.head(10)
            colors = ['red' if x < 0 else 'blue' for x in top_features.values]
            
            plt.barh(range(len(top_features)), top_features.values, color=colors)
            plt.yticks(range(len(top_features)), top_features.index)
            plt.xlabel('Correlation with Target')
            plt.title('Top 10 Features Correlated with Hit Songs')
            plt.grid(axis='x', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.figures_path / 'feature_correlations.png', dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Saved feature correlations plot")
    
    def plot_model_comparison(self, results):
        """Plot comparison of model performances."""
        models = list(results.keys())
        accuracies = [results[model]['accuracy'] for model in models]
        cv_scores = [results[model]['cv_mean'] for model in models]
        
        x = np.arange(len(models))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar(x - width/2, accuracies, width, label='Test Accuracy', alpha=0.8)
        bars2 = ax.bar(x + width/2, cv_scores, width, label='CV Accuracy', alpha=0.8)
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Accuracy')
        ax.set_title('Model Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{height:.3f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("Saved model comparison plot")
    
    def plot_feature_importance(self, model, feature_names, model_name):
        """Plot feature importance for tree-based models."""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 8))
            plt.title(f'Feature Importance - {model_name}')
            plt.bar(range(15), importances[indices][:15])
            plt.xticks(range(15), [feature_names[i] for i in indices[:15]], rotation=45, ha='right')
            plt.tight_layout()
            
            filename = self.figures_path / f'feature_importance_{model_name.lower().replace(" ", "_")}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            logger.info(f"Saved feature importance plot for {model_name}")
    
    def create_comprehensive_plots(self, df, results):
        """Create all comprehensive visualizations."""
        logger.info("Creating comprehensive visualizations...")
        
        self.plot_target_distribution(df)
        self.plot_feature_correlations(df)
        self.plot_model_comparison(results)
        
        # Plot feature importance for tree-based models
        feature_columns = [col for col in df.columns if col not in ['target', 'decade']]
        for model_name, result in results.items():
            model = result['model']
            self.plot_feature_importance(model, feature_columns, model_name)
        
        logger.info("All visualizations created successfully")