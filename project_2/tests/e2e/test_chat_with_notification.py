# tests/e2e/test_chat_with_notification.py

"""End-to-end tests between chat-service and notification-service.

This module tests the full flow of sending messages via chat-service
and verifying that notification-service writes the correct data to DynamoDB.
"""

import pytest
import httpx
import boto3
import asyncio

BASE_URL = "http://localhost:8001"

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
async def test_create_message_and_check_notification_in_dynamodb():
    """Send a plain text message and verify notification is saved in DynamoDB."""
    # Prepare the form data (plain text message, no media)
    data = {
        "chat_id": "1",
        "sender_sub": "test-sub-123",
        "content": "Hello from integration test!"
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data)

    # Verify HTTP response
    assert response.status_code == 200
    message_data = response.json()
    assert message_data["content"] == data["content"]

    # Wait briefly to allow notification-service to save data
    await asyncio.sleep(0.1)

    # Query DynamoDB for saved notification
    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan_response = table.scan()
    items = scan_response.get("Items", [])
    assert items, "No notifications found in DynamoDB"

    # Find the inserted notification by matching the message content
    matching = [item for item in items if data["content"] in item["message"]]
    assert matching, "Notification with the message content not found in DynamoDB"

    notification = matching[0]
    print("Notification found:", notification)

    # Validate notification fields
    assert notification["user_email"] == "lazar.jonasz@gmail.com"
    assert "From:" in notification["message"]
    assert "Contains media: No" in notification["message"]


@pytest.mark.asyncio
async def test_create_message_with_media_notification():
    """Send a message with both text and media, verify notification in DynamoDB."""
    # Prepare multipart form data (text + media)
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "content": (None, "This message has an image"),
        "media_file": ("test.jpg", b"fake image content", "image/jpeg")
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", files=files)

    # Verify HTTP response
    assert response.status_code == 200

    # Wait briefly to allow notification-service to save data
    await asyncio.sleep(0.1)

    # Query DynamoDB for saved notification
    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan_response = table.scan()
    items = scan_response.get("Items", [])

    # Find the notification by matching message content
    matching = [item for item in items if "This message has an image" in item["message"]]
    assert matching, "Notification with the message content not found"

    notification = matching[0]
    assert "Contains media: Yes" in notification["message"]


@pytest.mark.asyncio
async def test_create_message_media_only_notification():
    """Send a message with only media (no text), verify notification in DynamoDB."""
    # Prepare multipart form data (media only, no text)
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "media_file": ("only-media.jpg", b"fake image content", "image/jpeg")
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", files=files)

    # Verify HTTP response
    assert response.status_code == 200

    # Wait briefly to allow notification-service to save data
    await asyncio.sleep(0.1)

    # Query DynamoDB for saved notification
    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan_response = table.scan()
    items = scan_response.get("Items", [])

    # Find notification (by media file name or "No text" marker)
    matching = [item for item in items if "only-media.jpg" in item["message"] or "No text" in item["message"]]
    assert matching, "Notification for media-only message not found"

    notification = matching[0]
    assert "Message: [No text]" in notification["message"]
    assert "Contains media: Yes" in notification["message"]


@pytest.mark.asyncio
async def test_create_message_long_text_notification():
    """Send a message with very long text content and verify notification in DynamoDB."""
    long_text = "X" * 10000
    data = {
        "chat_id": "1",
        "sender_sub": "test-sub-123",
        "content": long_text
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data)

    # Verify HTTP response
    assert response.status_code == 200

    # Wait briefly to allow notification-service to save data
    await asyncio.sleep(0.1)

    # Query DynamoDB for saved notification
    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan_response = table.scan()
    items = scan_response.get("Items", [])

    # Check that part of the long text is present in notification message
    snippet = long_text[:100]
    matching = [item for item in items if snippet in item["message"]]
    assert matching, "Notification for long message not found"


@pytest.mark.asyncio
async def test_create_message_with_unicode_notification():
    """Send a message with Unicode characters and verify notification in DynamoDB."""
    unicode_text = "🚀🔥✨ Emoji test message with äöüß ñ Ćęść"
    data = {
        "chat_id": "1",
        "sender_sub": "test-sub-123",
        "content": unicode_text
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data)

    # Verify HTTP response
    assert response.status_code == 200

    # Wait briefly to allow notification-service to save data
    await asyncio.sleep(0.1)

    # Query DynamoDB for saved notification
    table = DYNAMODB.Table(NOTIFICATIONS_TABLE)
    scan_response = table.scan()
    items = scan_response.get("Items", [])

    matching = [item for item in items if "Emoji test message" in item["message"]]
    assert matching, "Notification for unicode message not found"

    notification = matching[0]
    assert "🚀" in notification["message"]
    assert "äöüß" in notification["message"]


@pytest.mark.asyncio
async def test_create_message_with_invalid_chat_id():
    """Test sending a message with a non-existent chat_id; expect 404 Not Found."""
    data = {
        "chat_id": "9999",  # Assuming this chat_id does not exist
        "sender_sub": "test-sub-123",
        "content": "Message for invalid chat"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data)

    assert response.status_code == 404
    assert "Chat not found" in response.text