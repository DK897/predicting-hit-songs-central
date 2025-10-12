"""
Unit tests for data loading functionality.
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Fix import path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data.data_loader import DataLoader

class TestDataLoader:
    def test_data_loader_initialization(self):
        """Test DataLoader initialization."""
        loader = DataLoader()
        assert str(loader.data_path) == "data/raw"
        assert str(loader.processed_path) == "data/processed"
        print("✅ DataLoader initialization test passed")
    
    def test_preprocess_data(self):
        """Test data preprocessing functionality."""
        # Create sample data
        sample_data = pd.DataFrame({
            'target': [1, 0, 1, 0],
            'danceability': [0.8, 0.6, 0.7, 0.5],
            'energy': [0.9, 0.7, 0.8, 0.6],
            'decade': ['00s', '00s', '10s', '10s']
        })
        
        loader = DataLoader()
        processed_df = loader.preprocess_data(sample_data)
        
        assert 'target' in processed_df.columns
        assert len(processed_df) == 4
        print("✅ Data preprocessing test passed")

def run_tests():
    """Run all tests."""
    test_class = TestDataLoader()
    test_class.test_data_loader_initialization()
    test_class.test_preprocess_data()
    print("🎉 All tests passed!")

if __name__ == "__main__":
    run_tests()