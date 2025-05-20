# tests/chat-service/test_get_messages.py

import pytest
import httpx
import json

BASE_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_get_messages_valid_chat():
    """
    Test retrieving messages from a valid chat with messages.
    Assumes chat_id=1 exists, has messages, and the user is a participant.
    """
    payload = {"sub": "test-sub-123"}  # must be participant of chat_id=1
    headers = {"X-User-Payload": json.dumps(payload)}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/1", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "chat_id" in data[0]
        assert "sender_sub" in data[0]
        assert "sent_at" in data[0]


@pytest.mark.asyncio
async def test_get_messages_nonexistent_chat():
    """
    Test retrieving messages from a chat that does not exist.
    Should return 404.
    """
    payload = {"sub": "test-sub-123"}  # any valid user
    headers = {"X-User-Payload": json.dumps(payload)}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/9999", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_get_messages_invalid_chat_id():
    """
    Test with invalid chat_id type (e.g., string instead of int).
    Should return 422.
    """
    payload = {"sub": "test-sub-123"}
    headers = {"X-User-Payload": json.dumps(payload)}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/invalid", headers=headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_messages_empty_chat():
    """
    Test retrieving messages from a valid chat that has no messages yet.
    Should return an empty list.
    Assumes chat_id=4 exists, no messages, and the user is a participant.
    """
    payload = {"sub": "test-sub-empty"}  # must be participant of chat_id=4
    headers = {"X-User-Payload": json.dumps(payload)}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/4", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_messages_not_participant():
    """
    Test retrieving messages from a chat where the user is NOT a participant.
    Should return 403 Forbidden.
    Assumes chat_id=1 exists and test-sub-other is not a participant.
    """
    payload = {"sub": "test-sub-other"}
    headers = {"X-User-Payload": json.dumps(payload)}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/1", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "You are not a participant of this chat"


@pytest.mark.asyncio
async def test_get_messages_missing_header():
    """
    Test retrieving messages without providing the X-User-Payload header.
    Should return 422.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/1")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_messages_invalid_json_in_header():
    """
    Test with invalid JSON in X-User-Payload header.
    Should return 400.
    """
    headers = {"X-User-Payload": "not-a-json"}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/messages/1", headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid X-User-Payload header"
