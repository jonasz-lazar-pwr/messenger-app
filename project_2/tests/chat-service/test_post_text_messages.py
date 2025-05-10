# tests/chat-service/test_post_text_messages.py

import pytest
import httpx
import json

BASE_URL = "http://localhost:8001"


@pytest.mark.asyncio
async def test_create_text_message():
    """Test creating a valid text message.

    Sends a well-formed JSON payload with `chat_id` and `content`,
    plus X-User-Payload header containing sender_sub.

    Expected:
        - 200 OK
        - Response JSON includes correct chat_id, sender_sub, and content.
    """
    data = {
        "chat_id": 1,
        "content": "Test message content"
    }
    token_payload = {"sub": "test-sub-123"}

    headers = {
        "X-User-Payload": json.dumps(token_payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["chat_id"] == data["chat_id"]
    assert data_out["sender_sub"] == token_payload["sub"]
    assert data_out["content"] == data["content"]


@pytest.mark.asyncio
async def test_empty_content_should_fail():
    """Test creating a text message with empty content.

    Sends a payload where `content` is an empty string.

    Expected:
        - 400 Bad Request
    """
    data = {
        "chat_id": 1,
        "content": ""
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-123"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_x_user_payload_header_should_fail():
    """Test creating a text message without X-User-Payload header.

    Expected:
        - 422 Unprocessable Entity (missing header)
    """
    data = {
        "chat_id": 1,
        "content": "Message without token header"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_chat_id_type_should_fail():
    """Test creating a text message with invalid chat_id type.

    Sets `chat_id` as a string instead of an integer.

    Expected:
        - 422 Unprocessable Entity
    """
    data = {
        "chat_id": "one",
        "content": "Invalid chat_id type"
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-123"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

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
        "content": "A" * 10000
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-123"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nonexistent_chat_id_should_fail_text():
    """Test creating a text message with a non-existent chat_id.

    Expected:
        - 404 Not Found
    """
    data = {
        "chat_id": 9999,
        "content": "Valid message but invalid chat_id"
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-123"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_chat_id_should_fail_text():
    """Test creating a text message without chat_id.

    Expected:
        - 422 Unprocessable Entity
    """
    data = {
        "content": "Missing chat_id"
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-123"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_json_in_token_header_should_fail():
    """Test with invalid JSON in X-User-Payload header.

    Expected:
        - 400 Bad Request
    """
    data = {
        "chat_id": 1,
        "content": "Message content"
    }
    headers = {
        "X-User-Payload": "not-a-json"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_user_not_in_chat_should_fail():
    """Test creating a text message when the sender is not part of the chat.

    Expected:
        - 403 Forbidden
    """
    data = {
        "chat_id": 1,
        "content": "Trying to send as unauthorized user"
    }
    headers = {
        "X-User-Payload": json.dumps({"sub": "test-sub-not-in-chat"})
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/messages/text", json=data, headers=headers)

    assert response.status_code == 403
