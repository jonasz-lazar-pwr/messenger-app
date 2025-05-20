# tests/media-service/run_media_tests.py

import pytest
import sys
from pathlib import Path

if __name__ == "__main__":
    media_tests_dir = Path(__file__).parent
    sys.exit(pytest.main([str(media_tests_dir)]))
