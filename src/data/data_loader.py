"""
Data loading and preprocessing utilities for hit song prediction.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, data_path="data/raw", processed_path="data/processed"):
        self.data_path = Path(data_path)
        self.processed_path = Path(processed_path)
        
    def load_processed_data(self):
        """Load already processed train and test datasets."""
        train_file = self.processed_path / "train_dataset.csv"
        test_file = self.processed_path / "test_dataset.csv"
        
        if train_file.exists() and test_file.exists():
            logger.info("Loading pre-processed train and test datasets...")
            train_df = pd.read_csv(train_file)
            test_df = pd.read_csv(test_file)
            
            # Combine for full dataset analysis
            combined_df = pd.concat([train_df, test_df], ignore_index=True)
            
            # Add decade column if it doesn't exist (for compatibility)
            if 'decade' not in combined_df.columns:
                # Extract decade from track names or add placeholder
                combined_df['decade'] = '00s'  # Placeholder
                train_df['decade'] = '00s'
                test_df['decade'] = '00s'
                
            logger.info(f"Loaded {len(train_df)} training and {len(test_df)} test samples")
            return combined_df, train_df, test_df
        else:
            logger.warning("Processed datasets not found, checking for raw decade files...")
            return self.load_from_raw_files()
    
    def load_from_raw_files(self):
        """Load and combine raw decade files."""
        decade_files = [f for f in os.listdir(self.data_path) if f.startswith('dataset-of-')]
        
        if not decade_files:
            # If no decade files, check if we have any CSV files
            all_csv_files = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]
            if all_csv_files:
                logger.info(f"No decade files found, but found {len(all_csv_files)} other CSV files")
                # Try to load the first CSV file as fallback
                file_path = self.data_path / all_csv_files[0]
                df = pd.read_csv(file_path)
                if 'decade' not in df.columns:
                    df['decade'] = 'unknown'
                processed_df = self.preprocess_data(df)
                return processed_df, None, None
            else:
                raise FileNotFoundError(f"No data files found in {self.data_path}")
        
        dataframes = []
        for file in decade_files:
            file_path = self.data_path / file
            logger.info(f"Loading {file}...")
            
            df = pd.read_csv(file_path)
            decade = file.split('-')[-1].split('.')[0]
            df['decade'] = decade
            
            dataframes.append(df)
        
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info(f"Combined {len(combined_df)} songs from {len(decade_files)} decades")
        
        # Preprocess the data
        processed_df = self.preprocess_data(combined_df)
        
        return processed_df, None, None
    
    def preprocess_data(self, df):
        """Clean and preprocess the combined dataset."""
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        if initial_count != len(df):
            logger.info(f"Removed {initial_count - len(df)} duplicates")
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Ensure target column exists
        if 'target' not in df.columns:
            # Look for alternative target columns
            possible_targets = ['hit', 'popular', 'chart']
            for col in possible_targets:
                if col in df.columns:
                    df = df.rename(columns={col: 'target'})
                    break
        
        if 'target' not in df.columns:
            # If no target column, create a dummy one for testing
            logger.warning("No target column found, creating dummy target")
            df['target'] = np.random.choice([0, 1], size=len(df), p=[0.7, 0.3])
        
        logger.info(f"Target distribution: {df['target'].value_counts().to_dict()}")
        return df

# Utility function for quick loading
def load_data():
    """Load data - prefers processed data if available."""
    loader = DataLoader()
    return loader.load_processed_data()