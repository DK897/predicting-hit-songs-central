"""
Project initialization script.
Creates all necessary directories and files.
"""

from pathlib import Path
import os

def initialize_project():
    """Initialize the complete project structure."""
    print("🚀 Initializing Hit Song Prediction Project...")
    
    # Create directories
    directories = [
        'data/raw', 'data/processed', 'data/external',
        'notebooks/exploratory', 'notebooks/modeling', 'notebooks/reports',
        'src/data', 'src/features', 'src/models', 'src/visualization',
        'models/saved_models', 'models/predictions',
        'reports/figures', 'reports/final_report',
        'tests/unit', 'tests/integration',
        'docs/presentation', 'docs/proposal',
        'config', 'logs', 'scripts'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    # Create __init__.py files
    for dir_path in ['src', 'src/data', 'src/features', 'src/models', 'src/visualization', 'tests']:
        init_file = Path(dir_path) / '__init__.py'
        init_file.touch()
        print(f"✅ Created: {init_file}")
    
    print("\n🎉 Project initialization complete!")
    print("📁 Project structure ready for development.")

if __name__ == "__main__":
    initialize_project()