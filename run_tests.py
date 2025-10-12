"""
Simple test runner for the project.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_all_tests():
    """Run all tests in the project."""
    print("🧪 Running Project Tests")
    print("=" * 40)
    
    try:
        # Import and run data loader tests
        from tests.test_data_loader import TestDataLoader
        
        test_class = TestDataLoader()
        test_class.test_data_loader_initialization()
        test_class.test_preprocess_data()
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_all_tests()