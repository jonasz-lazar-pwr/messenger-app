# tests/e2e/test_chat_to_notification.py

"""
End-to-end tests between chat-service and notification-service (DynamoDB validation).

This module tests sending text and media messages via chat-service
and verifies that notification-service writes the correct data to DynamoDB.
"""

import pytest
import httpx
import boto3
import asyncio

CHAT_BASE_URL = "http://localhost:8000"
DYNAMODB = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)
NOTIFICATIONS_TABLE = "Notifications"


@pytest.mark.asyncio
async def test_send_text_message_and_check_notification():
    """Send a text-only message and verify notification in DynamoDB."""
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "New E2E text message!"
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/text", json=payload)

    assert response.status_code == 200
    message_data = response.json()
    assert message_data["content"] == payload["content"]

    await asyncio.sleep(0.1)  # Allow time for DynamoDB write

    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan = table.scan()
    items = scan.get("Items", [])
    matching = [item for item in items if payload["content"] in item["message"]]
    assert matching, "Notification not found in DynamoDB"
    notification = matching[0]
    assert "Contains media: No" in notification["message"]


@pytest.mark.asyncio
async def test_send_media_message_and_check_notification():
    """Send a media-only message and verify notification in DynamoDB."""
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "media_file": ("image_e2e.jpg", b"fake image content", "image/jpeg")
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 200
    await asyncio.sleep(0.1)

    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan = table.scan()
    items = scan.get("Items", [])

    # Szukamy wzorca media-only (Message: [No text] + Contains media: Yes)
    matching = [
        item for item in items
        if "Message: [No text]" in item["message"]
        and "Contains media: Yes" in item["message"]
    ]

    assert matching, "Media-only notification not found in DynamoDB"

    notification = matching[0]
    # Opcjonalnie dodatkowe asercje dla kompletności
    assert "You have received a new message" in notification["message"]
    assert "From:" in notification["message"]
    assert "Contains media: Yes" in notification["message"]


@pytest.mark.asyncio
async def test_send_long_text_message_notification():
    """Send a message with very long text and verify notification."""
    long_text = "X" * 10000
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": long_text
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/text", json=payload)

    assert response.status_code == 200
    await asyncio.sleep(0.1)

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
        "sender_sub": "test-sub-123",
        "content": unicode_text
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/text", json=payload)

    assert response.status_code == 200
    await asyncio.sleep(0.1)

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
        "sender_sub": "test-sub-123",
        "content": "This should fail"
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/text", json=payload)

    assert response.status_code == 404
    assert "Chat not found" in response.text