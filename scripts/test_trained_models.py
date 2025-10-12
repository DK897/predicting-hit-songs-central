"""
Test trained models and make predictions.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure repository root is on sys.path so we can import `src` (script may be run from scripts/)
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.data.data_loader import DataLoader
from src.features.feature_engineer import FeatureEngineer
from src.models.model_evaluator import ModelEvaluator

def load_trained_models():
    """Load all trained models from the models directory."""
    models_path = Path("models/saved_models")
    models = {}
    
    if not models_path.exists():
        print("❌ No trained models found. Please train models first.")
        return None
    
    model_files = list(models_path.glob("*.pkl"))
    
    if not model_files:
        print("❌ No model files found in models/saved_models/")
        return None
    
    print(f"🔍 Found {len(model_files)} trained models:")
    for model_file in model_files:
        try:
            model_name = model_file.stem.replace('_', ' ').title()
            model = joblib.load(model_file)
            models[model_name] = model
            print(f"   ✅ {model_name}")
        except Exception as e:
            print(f"   ❌ Error loading {model_file.name}: {e}")
    
    return models

def test_models_on_data(models, X_test, y_test, feature_columns):
    """Test all models on test data and return results."""
    results = {}
    evaluator = ModelEvaluator()
    
    print(f"\n🎯 Testing Models on {len(X_test)} samples")
    print("=" * 50)
    
    for model_name, model in models.items():
        print(f"\n🧪 Testing {model_name}...")
        
        try:
            # Prepare features (scale if needed for SVM/Neural Network)
            if any(keyword in model_name.lower() for keyword in ['svm', 'neural']):
                from sklearn.preprocessing import StandardScaler
                scaler = StandardScaler()
                X_test_scaled = scaler.fit_transform(X_test)
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else None
            else:
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            # Store results
            results[model_name] = {
                'model': model,
                'accuracy': accuracy,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'y_test': y_test
            }
            
            print(f"   ✅ Accuracy: {accuracy:.3f}")
            
            # Generate detailed report for the best performing models
            if accuracy > 0.6:  # Only for reasonably good models
                evaluator.generate_detailed_report(y_test, y_pred, y_pred_proba, model_name)
            
        except Exception as e:
            print(f"   ❌ Error testing {model_name}: {e}")
    
    return results

def make_predictions_on_new_data(models, feature_engineer, reference_feature_columns):
    """Make predictions on new sample data."""
    print(f"\n🎵 Making Predictions on Sample Songs")
    print("=" * 50)
    
    # Create sample song data
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
    
    sample_df = pd.DataFrame(sample_songs)
    
    # Apply feature engineering
    sample_features = feature_engineer.create_features(sample_df)

    # Ensure the sample features have the same columns that models were trained on
    # Missing columns (e.g., one-hot decade columns) will be filled with zeros
    X_sample = sample_features.reindex(columns=reference_feature_columns, fill_value=0)
    
    print("Sample Song 1 (High energy, danceable):")
    for model_name, model in models.items():
        try:
            if any(keyword in model_name.lower() for keyword in ['svm', 'neural']):
                from sklearn.preprocessing import StandardScaler
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X_sample)
                # X_scaled is a numpy array; index with [[]]
                prediction = model.predict(X_scaled[[0]])[0]
                probability = model.predict_proba(X_scaled[[0]])[0, 1] if hasattr(model, "predict_proba") else None
            else:
                # For tree-based models, pass a DataFrame row
                prediction = model.predict(X_sample.iloc[[0]])[0]
                probability = model.predict_proba(X_sample.iloc[[0]])[0, 1] if hasattr(model, "predict_proba") else None
            
            result = "HIT 🎵" if prediction == 1 else "Non-hit"
            confidence = f" ({probability:.1%})" if probability is not None else ""
            print(f"   {model_name}: {result}{confidence}")
            
        except Exception as e:
            print(f"   {model_name}: Error - {e}")
    
    print("\nSample Song 2 (Low energy, acoustic):")
    for model_name, model in models.items():
        try:
            if any(keyword in model_name.lower() for keyword in ['svm', 'neural']):
                from sklearn.preprocessing import StandardScaler
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X_sample)
                prediction = model.predict(X_scaled[[1]])[0]
                probability = model.predict_proba(X_scaled[[1]])[0, 1] if hasattr(model, "predict_proba") else None
            else:
                prediction = model.predict(X_sample.iloc[[1]])[0]
                probability = model.predict_proba(X_sample.iloc[[1]])[0, 1] if hasattr(model, "predict_proba") else None
            
            result = "HIT 🎵" if prediction == 1 else "Non-hit"
            confidence = f" ({probability:.1%})" if probability is not None else ""
            print(f"   {model_name}: {result}{confidence}")
            
        except Exception as e:
            print(f"   {model_name}: Error - {e}")

def analyze_feature_importance(models, feature_columns):
    """Analyze feature importance for tree-based models."""
    print(f"\n🔍 Feature Importance Analysis")
    print("=" * 50)
    
    for model_name, model in models.items():
        if hasattr(model, 'feature_importances_'):
            print(f"\n📊 {model_name} Feature Importance:")
            importances = model.feature_importances_
            
            # Create feature importance dataframe
            importance_df = pd.DataFrame({
                'feature': feature_columns,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            # Display top 10 features
            for i, row in importance_df.head(10).iterrows():
                print(f"   {row['feature']}: {row['importance']:.3f}")
            
            # Plot feature importance
            plt.figure(figsize=(10, 6))
            sns.barplot(data=importance_df.head(15), x='importance', y='feature')
            plt.title(f'Top 15 Feature Importance - {model_name}')
            plt.tight_layout()
            plt.savefig(f'reports/figures/feature_importance_{model_name.lower().replace(" ", "_")}.png', 
                       dpi=300, bbox_inches='tight')
            plt.close()

def main():
    print("🎵 Testing Trained Hit Song Prediction Models")
    print("=" * 60)
    
    # Load trained models
    models = load_trained_models()
    if not models:
        return
    
    # Load test data
    print(f"\n📁 Loading test data...")
    loader = DataLoader()
    combined_df, train_df, test_df = loader.load_processed_data()
    
    # If we have separate test data, use it. Otherwise, create a test split
    if test_df is not None:
        print("Using pre-existing test dataset")
        test_data = test_df
    else:
        print("Creating test split from combined data")
        from sklearn.model_selection import train_test_split
        test_data = combined_df.sample(frac=0.25, random_state=42)
    
    # Feature engineering
    feature_engineer = FeatureEngineer()
    features_df = feature_engineer.create_features(test_data)
    
    # Prepare features for testing
    exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
    feature_columns = [col for col in features_df.columns if col not in exclude_cols]
    
    X_test = features_df[feature_columns]
    y_test = features_df['target']
    
    # Test models
    results = test_models_on_data(models, X_test, y_test, feature_columns)
    
    if results:
        # Find best model
        best_model_name = max(results.keys(), key=lambda x: results[x]['accuracy'])
        best_accuracy = results[best_model_name]['accuracy']
        
        print(f"\n🏆 BEST MODEL: {best_model_name}")
        print(f"🎯 ACCURACY: {best_accuracy:.1%}")
        
        # Feature importance analysis
        analyze_feature_importance(models, feature_columns)
        
        # Make predictions on sample data
        make_predictions_on_new_data(models, feature_engineer)
        
        print(f"\n✅ Model testing completed!")
        print(f"📊 Check 'reports/figures/' for detailed analysis charts")
    else:
        print("❌ No models were successfully tested")

if __name__ == "__main__":
    main()
