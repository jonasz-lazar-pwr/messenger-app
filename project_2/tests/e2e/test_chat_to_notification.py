# tests/e2e/test_chat_to_notification.py

import pytest
import httpx
import boto3
import asyncio
import json

CHAT_BASE_URL = "http://localhost:8001"
DYNAMODB = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)
NOTIFICATIONS_TABLE = "Notifications"

# Sample payload to mimic X-User-Payload (token payload)
X_USER_PAYLOAD = json.dumps({
    "sub": "test-sub-123",
    "email": "user@example.com",
    "given_name": "Test",
    "family_name": "User"
})


@pytest.mark.asyncio
async def test_send_text_message_and_check_notification():
    """Send a text-only message and verify notification in DynamoDB."""
    payload = {
        "chat_id": 1,
        "content": "New E2E text message!"
    }
    headers = {"X-User-Payload": X_USER_PAYLOAD}

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/messages/text", json=payload, headers=headers)

    assert response.status_code == 200
    message_data = response.json()
    assert message_data["content"] == payload["content"]

    await asyncio.sleep(0.2)  # Allow time for DynamoDB write

    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan = table.scan()
    items = scan.get("Items", [])
    matching = [item for item in items if payload["content"] in item["message"]]
    assert matching, "Notification not found in DynamoDB"
    notification = matching[0]
    assert "Contains media: No" in notification["message"]


@pytest.mark.asyncio
async def test_send_long_text_message_notification():
    """Send a message with very long text and verify notification."""
    long_text = "X" * 10000
    payload = {
        "chat_id": 1,
        "content": long_text
    }
    headers = {"X-User-Payload": X_USER_PAYLOAD}

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/messages/text", json=payload, headers=headers)

    assert response.status_code == 200
    await asyncio.sleep(0.2)

    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan = table.scan()
    items = scan.get("Items", [])
    snippet = long_text[:100]
    matching = [item for item in items if snippet in item["message"]]
    assert matching, "Notification for long message not found"


@pytest.mark.asyncio
async def test_send_unicode_text_message_notification():
    """Send a message with Unicode and verify notification."""
    unicode_text = "🚀🔥 Test message with emoji äöüß ñ Ćęść"
    payload = {
        "chat_id": 1,
        "content": unicode_text
    }
    headers = {"X-User-Payload": X_USER_PAYLOAD}

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/messages/text", json=payload, headers=headers)

    assert response.status_code == 200
    await asyncio.sleep(0.2)

    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan = table.scan()
    items = scan.get("Items", [])
    matching = [item for item in items if "Test message with emoji" in item["message"]]
    assert matching, "Notification for Unicode message not found"
    notification = matching[0]
    assert "🚀" in notification["message"]


@pytest.mark.asyncio
async def test_send_invalid_chat_id_notification():
    """Send message to invalid chat_id and expect 404."""
    payload = {
        "chat_id": 9999,
        "content": "This should fail"
    }
    headers = {"X-User-Payload": X_USER_PAYLOAD}

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/messages/text", json=payload, headers=headers)

    assert response.status_code == 404
    assert "Chat not found" in response.text
