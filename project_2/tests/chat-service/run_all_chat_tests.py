# tests/chat-service/run_all_chat_tests.py

import pytest
import sys
from pathlib import Path

if __name__ == "__main__":
    chat_tests_dir = Path(__file__).parent
    sys.exit(pytest.main([str(chat_tests_dir)]))
