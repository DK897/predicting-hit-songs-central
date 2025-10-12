"""
Model training for hit song prediction.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import joblib
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.results = {}
        self.models_path = Path("models/saved_models")
        self.models_path.mkdir(parents=True, exist_ok=True)
        
    def initialize_models(self):
        """Initialize all machine learning models."""
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, random_state=42),
            'Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42, max_iter=1000),
            'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
        }
        logger.info(f"Initialized {len(self.models)} models")
    
    def prepare_features(self, df):
        """Prepare features and target for modeling."""
        # Exclude non-feature columns
        exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
        feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_columns]
        y = df['target']
        
        # Handle any remaining missing values
        X = X.fillna(X.median())
        
        logger.info(f"Prepared features: {X.shape[1]} features, {len(y)} samples")
        return X, y, feature_columns
    
    def train_all_models(self, df, train_indices=None, test_indices=None):
        """Train all models and evaluate performance."""
        self.initialize_models()
        
        # Prepare data
        X, y, feature_columns = self.prepare_features(df)
        
        # Use pre-defined split or create new split
        if train_indices is not None and test_indices is not None:
            X_train = X.iloc[train_indices]
            X_test = X.iloc[test_indices]
            y_train = y.iloc[train_indices]
            y_test = y.iloc[test_indices]
            logger.info(f"Using pre-split data: Train={X_train.shape[0]}, Test={X_test.shape[0]}")
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.25, random_state=42, stratify=y
            )
            logger.info(f"Created new split: Train={X_train.shape[0]}, Test={X_test.shape[0]}")
        
        # Train and evaluate each model
        for name, model in self.models.items():
            logger.info(f"Training {name}...")
            
            try:
                # Use scaled features for SVM and Neural Network
                if name in ['SVM', 'Neural Network']:
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
                
                # Store results
                self.results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'predictions': y_pred,
                    'probabilities': y_pred_proba,
                    'feature_importance': getattr(model, 'feature_importances_', None),
                    'y_test': y_test
                }
                
                # Save model
                self.save_model(model, name)
                
                logger.info(f"{name} - Accuracy: {accuracy:.3f}, CV: {cv_scores.mean():.3f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {e}")
        
        return self.results
    
    def train_with_pre_split_data(self, features_df, train_indices, test_indices):
        """Train models with pre-defined train/test split."""
        self.initialize_models()
        
        # Prepare features
        exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
        feature_columns = [col for col in features_df.columns if col not in exclude_cols]
        
        X = features_df[feature_columns]
        y = features_df['target']
        
        # Handle any remaining missing values
        X = X.fillna(X.median())
        
        # Use pre-defined split
        X_train = X.iloc[train_indices]
        X_test = X.iloc[test_indices]
        y_train = y.iloc[train_indices]
        y_test = y.iloc[test_indices]
        
        logger.info(f"Using pre-split data: Train={X_train.shape[0]}, Test={X_test.shape[0]}")
        
        # Train and evaluate each model
        for name, model in self.models.items():
            logger.info(f"Training {name}...")
            
            try:
                # Use scaled features for SVM and Neural Network
                if name in ['SVM', 'Neural Network']:
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
                
                # Store results
                self.results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'predictions': y_pred,
                    'probabilities': y_pred_proba,
                    'feature_importance': getattr(model, 'feature_importances_', None),
                    'y_test': y_test
                }
                
                # Save model
                self.save_model(model, name)
                
                logger.info(f"{name} - Accuracy: {accuracy:.3f}, CV: {cv_scores.mean():.3f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {e}")
        
        return self.results
    
    def save_model(self, model, name):
        """Save trained model to file."""
        filename = self.models_path / f"{name.lower().replace(' ', '_')}.pkl"
        joblib.dump(model, filename)
        logger.info(f"Saved model: {filename}")
    
    def load_model(self, name):
        """Load trained model from file."""
        filename = self.models_path / f"{name.lower().replace(' ', '_')}.pkl"
        if filename.exists():
            return joblib.load(filename)
        else:
            raise FileNotFoundError(f"Model {name} not found")
    
    def get_best_model(self):
        """Get the best performing model based on accuracy."""
        if not self.results:
            raise ValueError("No models trained yet")
        
        best_model_name = max(self.results.keys(), key=lambda x: self.results[x]['accuracy'])
        return best_model_name, self.results[best_model_name]