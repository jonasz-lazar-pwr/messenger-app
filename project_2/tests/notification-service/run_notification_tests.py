# tests/notification-service/run_notification_tests.py

import pytest
import sys
from pathlib import Path

if __name__ == "__main__":
    notification_tests_dir = Path(__file__).parent
    sys.exit(pytest.main([str(notification_tests_dir)]))
