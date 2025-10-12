"""
Utility to help with import paths across the project.
"""

import sys
import os
from pathlib import Path

def setup_project_imports():
    """Add project root to Python path for all modules."""
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return project_root

# Run this when the module is imported
setup_project_imports()