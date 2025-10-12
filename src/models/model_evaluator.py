"""
Model evaluation and metrics calculation.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix, classification_report, 
                           roc_auc_score, roc_curve, precision_recall_curve)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self):
        self.figures_path = Path("reports/figures")
        self.figures_path.mkdir(parents=True, exist_ok=True)
    
    def calculate_metrics(self, y_true, y_pred, y_proba=None):
        """Calculate comprehensive evaluation metrics."""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0)
        }
        
        if y_proba is not None:
            try:
                metrics['roc_auc'] = roc_auc_score(y_true, y_proba)
            except Exception:
                metrics['roc_auc'] = 0.0
        
        return metrics
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """Plot confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Non-Hit', 'Hit'], 
                   yticklabels=['Non-Hit', 'Hit'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        
        filename = self.figures_path / f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved confusion matrix for {model_name}")
    
    def plot_roc_curve(self, y_true, y_proba, model_name):
        """Plot ROC curve."""
        if y_proba is None:
            logger.warning(f"No probabilities available for ROC curve - {model_name}")
            return 0.0
            
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_auc = roc_auc_score(y_true, y_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        
        filename = self.figures_path / f'roc_curve_{model_name.lower().replace(" ", "_")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved ROC curve for {model_name}")
        
        return roc_auc
    
    def generate_detailed_report(self, y_true, y_pred, y_proba, model_name):
        """Generate detailed evaluation report."""
        metrics = self.calculate_metrics(y_true, y_pred, y_proba)
        
        print(f"\n📊 Detailed Report - {model_name}")
        print("=" * 50)
        for metric, value in metrics.items():
            print(f"{metric.capitalize()}: {value:.3f}")
        
        print(f"\n📈 Classification Report:")
        print(classification_report(y_true, y_pred, target_names=['Non-Hit', 'Hit'], zero_division=0))
        
        # Plot visualizations
        self.plot_confusion_matrix(y_true, y_pred, model_name)
        if y_proba is not None:
            self.plot_roc_curve(y_true, y_proba, model_name)
        
        return metrics