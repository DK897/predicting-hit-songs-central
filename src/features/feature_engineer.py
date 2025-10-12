"""
Feature engineering for hit song prediction.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA()
        
    def create_interaction_features(self, df):
        """Create feature interactions."""
        features_df = df.copy()
        
        # Audio feature interactions
        audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                         'instrumentalness', 'liveness', 'speechiness']
        
        available_audio = [f for f in audio_features if f in df.columns]
        
        for feat in available_audio:
            for other_feat in available_audio:
                if feat != other_feat:
                    features_df[f'{feat}_{other_feat}_ratio'] = (
                        df[feat] / (df[other_feat] + 1e-8)
                    )
        
        # Energy-danceability composite
        if 'danceability' in df.columns and 'energy' in df.columns:
            features_df['energy_dance_composite'] = df['energy'] * df['danceability']
        
        # Acoustic-energy ratio
        if 'acousticness' in df.columns and 'energy' in df.columns:
            features_df['acoustic_energy_ratio'] = df['acousticness'] / (df['energy'] + 1e-8)
        
        return features_df
    
    def create_temporal_features(self, df):
        """Create temporal and duration-based features."""
        features_df = df.copy()
        
        if 'duration_ms' in df.columns:
            # Convert to minutes
            features_df['duration_minutes'] = df['duration_ms'] / 60000
            
            # Duration categories
            features_df['is_short_song'] = (features_df['duration_minutes'] < 3).astype(int)
            features_df['is_medium_song'] = (
                (features_df['duration_minutes'] >= 3) & 
                (features_df['duration_minutes'] <= 5)
            ).astype(int)
            features_df['is_long_song'] = (features_df['duration_minutes'] > 5).astype(int)
        
        return features_df
    
    def create_decade_features(self, df):
        """Create decade-based features."""
        features_df = df.copy()
        
        if 'decade' in df.columns:
            # One-hot encode decades
            decade_dummies = pd.get_dummies(df['decade'], prefix='decade')
            features_df = pd.concat([features_df, decade_dummies], axis=1)
        
        return features_df
    
    def scale_features(self, df, feature_columns):
        """Scale numerical features."""
        features_df = df.copy()
        
        # Scale only numerical features
        numerical_features = features_df[feature_columns].select_dtypes(include=[np.number]).columns
        features_df[numerical_features] = self.scaler.fit_transform(features_df[numerical_features])
        
        return features_df
    
    def create_features(self, df):
        """Complete feature engineering pipeline."""
        logger.info("Starting feature engineering...")
        
        # Step 1: Create interaction features
        features_df = self.create_interaction_features(df)
        logger.info(f"Created interaction features. Total features: {len(features_df.columns)}")
        
        # Step 2: Create temporal features
        features_df = self.create_temporal_features(features_df)
        logger.info(f"Created temporal features. Total features: {len(features_df.columns)}")
        
        # Step 3: Create decade features
        features_df = self.create_decade_features(features_df)
        logger.info(f"Created decade features. Total features: {len(features_df.columns)}")
        
        # Identify feature columns (exclude non-feature columns)
        exclude_cols = ['target', 'decade', 'uri', 'track', 'artist', 'id']
        feature_columns = [col for col in features_df.columns if col not in exclude_cols]
        
        # Step 4: Scale features
        features_df = self.scale_features(features_df, feature_columns)
        logger.info(f"Scaled features. Final feature count: {len(feature_columns)}")
        
        # Save feature list
        self.feature_columns = feature_columns
        logger.info(f"Feature engineering complete. Final dataset shape: {features_df.shape}")
        
        return features_df