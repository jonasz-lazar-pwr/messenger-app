# tests/e2e/run_e2e_tests.py

import pytest
import sys
from pathlib import Path

if __name__ == "__main__":
    e2e_tests_dir = Path(__file__).parent
    sys.exit(pytest.main([str(e2e_tests_dir)]))
