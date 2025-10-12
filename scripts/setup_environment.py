"""
Setup script to install all required dependencies and fix import paths.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install all required packages."""
    print("📦 Installing requirements...")
    
    requirements = [
        "pandas==1.5.3",
        "numpy==1.24.3", 
        "scikit-learn==1.2.2",
        "matplotlib==3.7.1",
        "seaborn==0.12.2",
        "jupyter==1.0.0",
        "xgboost==1.7.5",
        "librosa==0.10.0",
        "plotly==5.14.1",
        "tqdm==4.65.0",
        "joblib==1.2.0",
        "pytest==7.4.0"  # Add pytest for testing
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {package}")

def create_pythonpath_script():
    """Create a script to set Python path."""
    script_content = '''#!/bin/bash
# Set Python path for the project
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "Python path set for Hit Song Prediction project"
'''
    
    with open('set_pythonpath.sh', 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('set_pythonpath.sh', 0o755)
    print("✅ Created Python path setup script")

def main():
    print("🚀 Setting up Hit Song Prediction Project Environment")
    print("=" * 50)
    
    install_requirements()
    create_pythonpath_script()
    
    print("\n🎉 Environment setup complete!")
    print("📝 Next steps:")
    print("1. Run: source set_pythonpath.sh")
    print("2. Add your CSV files to data/raw/")
    print("3. Run: python notebooks/exploratory/01_data_exploration.py")

if __name__ == "__main__":
    main()