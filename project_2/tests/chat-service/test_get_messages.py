# tests/chat-service/test_get_messages.py

import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_get_messages_valid_chat():
    """
    Test retrieving messages from a valid chat with messages.
    Assumes chat_id=1 exists and has at least one message.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/messages/1")

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
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/messages/9999")  # non-existent chat

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"

@pytest.mark.asyncio
async def test_get_messages_invalid_chat_id():
    """
    Test with invalid chat_id type (e.g., string instead of int).
    Should return 422.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/messages/invalid")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_messages_empty_chat():
    """
    Test retrieving messages from a valid chat that has no messages yet.
    Should return an empty list.
    Assumes chat_id=4 exists and has no messages.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/messages/4")

    assert response.status_code == 200
    assert response.json() == []