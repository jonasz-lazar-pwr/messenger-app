# tests/chat-service/test_post_text_messages.py

"""Integration tests for the /messages/text endpoint of chat-service.

These tests validate the behavior of the text-only message creation endpoint,
ensuring it correctly handles valid and invalid input data.

Endpoint under test:
    POST /api/messages/text
"""

import pytest
import httpx

# Base URL for chat-service
BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_create_text_message():
    """Test creating a valid text message.

    Sends a well-formed JSON payload with `chat_id`, `sender_sub`,
    and `content`. Verifies the response status and content.

    Expected:
        - 200 OK
        - Response JSON includes correct chat_id, sender_sub, and content.
    """
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "Test message content"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["chat_id"] == int(data["chat_id"])
    assert data_out["sender_sub"] == data["sender_sub"]
    assert data_out["content"] == data["content"]


@pytest.mark.asyncio
async def test_empty_content_should_fail():
    """Test creating a text message with empty content.

    Sends a payload where `content` is an empty string.
    The API should reject it because content must be non-empty.

    Expected:
        - 400 Bad Request
    """
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": ""
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_missing_sender_sub_should_fail():
    """Test creating a text message without sender_sub.

    Omits the `sender_sub` field, which is required by the API.

    Expected:
        - 422 Unprocessable Entity (validation error)
    """
    data = {
        "chat_id": 1,
        "content": "Message without sender_sub"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_chat_id_type_should_fail():
    """Test creating a text message with invalid chat_id type.

    Sets `chat_id` as a string instead of an integer.
    The API should reject this as a validation error.

    Expected:
        - 422 Unprocessable Entity
    """
    data = {
        "chat_id": "one",
        "sender_sub": "test-sub-123",
        "content": "Invalid chat_id type"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_very_long_content():
    """Test creating a text message with very long content.

    Sends a message with 10,000 characters to test large payload handling.

    Expected:
        - 200 OK
    """
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "A" * 10000
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nonexistent_chat_id_should_fail_text():
    """Test creating a text message with a non-existent chat_id.

    Expected:
        - 404 Not Found
    """
    data = {
        "chat_id": 9999,
        "sender_sub": "test-sub-123",
        "content": "Valid message but invalid chat_id"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_chat_id_should_fail_text():
    """Test creating a text message without chat_id.

    Expected:
        - 422 Unprocessable Entity
    """
    data = {
        "sender_sub": "test-sub-123",
        "content": "Missing chat_id"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/text", json=data)

    assert response.status_code == 422
