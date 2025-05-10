# tests/chat-service/test_get_chats.py

import pytest
import httpx
import json

BASE_URL = "http://localhost:8001"


@pytest.mark.asyncio
async def test_get_chats_existing_user():
    """
    Test retrieving chats for an existing user who participates in at least one chat.
    """
    user_sub = "test-sub-123"
    headers = {"X-User-Payload": json.dumps({"sub": user_sub})}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        chat = data[0]
        assert "id" in chat
        assert "participant" in chat
        assert "first_name" in chat["participant"]
        assert "last_name" in chat["participant"]


@pytest.mark.asyncio
async def test_get_chats_user_with_no_chats():
    """
    Test retrieving chats for a user who exists but has no chats.
    """
    user_sub = "test-sub-nochats"
    headers = {"X-User-Payload": json.dumps({"sub": user_sub})}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_chats_missing_header():
    """
    Test calling the endpoint without the X-User-Payload header.
    Should return 422 Unprocessable Entity.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_chats_invalid_json_header():
    """
    Test calling the endpoint with invalid JSON in X-User-Payload header.
    Should return 400 Bad Request.
    """
    headers = {"X-User-Payload": "not-a-json"}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid X-User-Payload header"


@pytest.mark.asyncio
async def test_get_chats_missing_sub_in_payload():
    """
    Test calling the endpoint with JSON missing the 'sub' field.
    Should return 400 Bad Request.
    """
    headers = {"X-User-Payload": json.dumps({"email": "test@example.com"})}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Missing 'sub' in token payload"


@pytest.mark.asyncio
async def test_get_chats_user_with_multiple_chats():
    """
    Test user who is in multiple chats to ensure the endpoint returns all of them.
    """
    user_sub = "test-sub-multi"
    headers = {"X-User-Payload": json.dumps({"sub": user_sub})}

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/chats", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for chat in data:
        assert "id" in chat
        assert "participant" in chat
        assert "first_name" in chat["participant"]
        assert "last_name" in chat["participant"]
