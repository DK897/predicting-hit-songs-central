"""
Quick script to verify data loading and basic functionality.
"""

import pandas as pd
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    print("🔍 Quick Data Verification")
    print("=" * 40)
    
    # Check processed data
    processed_dir = Path("data/processed")
    if processed_dir.exists():
        print("✅ Processed data directory exists")
        files = list(processed_dir.glob("*.csv"))
        for file in files:
            try:
                df = pd.read_csv(file)
                print(f"   {file.name}: {len(df)} rows, {len(df.columns)} columns")
                if 'target' in df.columns:
                    hit_rate = df['target'].mean() * 100
                    print(f"     - Hit rate: {hit_rate:.1f}%")
                print(f"     - Columns: {list(df.columns)[:5]}...")  # Show first 5 columns
            except Exception as e:
                print(f"     - Error reading file: {e}")
    else:
        print("❌ Processed data directory not found")
    
    # Check raw data
    raw_dir = Path("data/raw")
    if raw_dir.exists():
        print("✅ Raw data directory exists")
        files = list(raw_dir.glob("dataset-of-*.csv"))
        print(f"   Found {len(files)} decade files")
        for file in files[:3]:  # Show first 3 files
            try:
                df = pd.read_csv(file)
                print(f"     - {file.name}: {len(df)} rows")
            except Exception as e:
                print(f"     - Error reading {file.name}: {e}")
    else:
        print("❌ Raw data directory not found")
    
    # Try to import and use DataLoader
    try:
        from src.data.data_loader import DataLoader
        loader = DataLoader()
        combined_df, train_df, test_df = loader.load_processed_data()
        
        print(f"\n📊 DataLoader Results:")
        print(f"   Combined data: {len(combined_df)} rows")
        if train_df is not None:
            print(f"   Train data: {len(train_df)} rows")
        if test_df is not None:
            print(f"   Test data: {len(test_df)} rows")
        
        print(f"   Features: {list(combined_df.columns)[:10]}...")  # Show first 10 features
        
    except Exception as e:
        print(f"❌ DataLoader error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()