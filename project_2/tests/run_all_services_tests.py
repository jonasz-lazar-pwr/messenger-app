# tests/run_all_services_tests.py

import subprocess

services = [
    "chat-service/run_all_chat_tests.py"
    # "media-service/run_all_media_tests.py",
    # "notification-service/run_all_notification_tests.py"
]

if __name__ == "__main__":
    for service_runner in services:
        print(f"Running tests for: {service_runner}")
        subprocess.run(["python", service_runner])