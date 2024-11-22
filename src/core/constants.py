from pathlib import Path
import sys

# Define PROJECT_ROOT dynamically based on the location of constants.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Ensure PROJECT_ROOT is in sys.path for module resolution
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
