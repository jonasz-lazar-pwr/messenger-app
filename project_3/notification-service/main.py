# === main.py ===

"""Main polling loop for the Notification Service.

This script continuously polls an SQS queue for notification messages,
sends notifications via SNS, and stores them in DynamoDB.

Environment Variables:
    - AWS_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN
    - AWS_SQS_NOTIFICATION_QUEUE_URL
    - AWS_SNS_TOPIC_ARN
"""

import json
import os
import time
from datetime import datetime
from uuid import uuid4

import boto3

from services.dynamo import save_notification
from services.sns import send_notification_to_sns

# Initialize SQS client
sqs = boto3.client(
    "sqs",
    region_name=os.environ["AWS_REGION"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ["AWS_SESSION_TOKEN"],
)

queue_url = os.environ.get("AWS_SQS_NOTIFICATION_QUEUE_URL")
if not queue_url:
    raise RuntimeError("Missing SQS queue URL")


def poll_sqs():
    """Continuously poll the SQS queue and process incoming messages.

    For each message received, this function will:
    - Parse the message body.
    - Send a notification via SNS.
    - Persist the notification in DynamoDB.
    - Remove the message from the SQS queue.
    """
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=10,
            )

            messages = response.get("Messages", [])
            if not messages:
                continue

            for msg in messages:
                try:
                    payload = json.loads(msg["Body"])
                    user_email = payload["user_email"]
                    message = payload["message"]

                    notification_id = str(uuid4())
                    sent_at = datetime.utcnow().isoformat()

                    send_notification_to_sns(user_email, message)
                    save_notification(notification_id, user_email, message, sent_at)

                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=msg["ReceiptHandle"],
                    )

                except Exception:
                    pass  # Silently skip to the next message

        except Exception:
            time.sleep(5)


if __name__ == "__main__":
    poll_sqs()
