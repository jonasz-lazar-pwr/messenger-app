# tests/chat-service/test_post_message.py

import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_create_text_message():
    """
    Test sending a valid plain text message.
    Assumes that chat_id = 1 and sender_sub = "test-sub-123" exist in the database.
    """
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "Test message content",
        "media_url": None,
        "media_id": None
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == payload["chat_id"]
    assert data["sender_sub"] == payload["sender_sub"]
    assert data["content"] == payload["content"]

@pytest.mark.asyncio
async def test_message_empty_content_and_no_media():
    """
    Test submitting a message without text or media.
    This should fail due to missing required content.
    """
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "",
        "media_url": None,
        "media_id": None
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_message_with_only_media():
    """
    Test sending a message with only media (no text content).
    This should succeed.
    """
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": None,
        "media_url": "http://example.com/image.jpg",
        "media_id": str(uuid4())
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["media_url"] == payload["media_url"]

@pytest.mark.asyncio
async def test_message_missing_sender_sub():
    """
    Test sending a message with missing sender_sub field.
    This should fail with validation error.
    """
    payload = {
        "chat_id": 1,
        "content": "Message",
        "media_url": None,
        "media_id": None
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_message_with_invalid_chat_id_type():
    """
    Test sending a message with a string instead of integer for chat_id.
    Should fail due to type validation.
    """
    payload = {
        "chat_id": "one",  # invalid type
        "sender_sub": "test-sub-123",
        "content": "Invalid chat_id type",
        "media_url": None,
        "media_id": None
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_message_with_very_long_content():
    """
    Test sending a message with very long content (e.g., 10,000 characters).
    This should succeed unless there are explicit length limits.
    """
    payload = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "A" * 10000,
        "media_url": None,
        "media_id": None
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", json=payload)

    assert response.status_code == 200