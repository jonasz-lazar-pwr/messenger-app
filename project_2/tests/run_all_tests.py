# tests/run_all_tests.py

import subprocess

services = [
    "chat-service/run_chat_tests.py",
    "media-service/run_media_tests.py",
    "notification-service/run_notification_tests.py",
    "e2e/run_e2e_tests.py",
]

if __name__ == "__main__":
    for service_runner in services:
        print(f"Running tests for: {service_runner}")
        subprocess.run(["python", service_runner])
