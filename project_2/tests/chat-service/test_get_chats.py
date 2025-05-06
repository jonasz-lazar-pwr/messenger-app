# tests/chat-service/test_get_chats.py

import pytest
import httpx

BASE_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_get_chats_existing_user():
    """
    Test retrieving chats for an existing user who participates in at least one chat.
    Assumes that user_sub="test-sub-123" exists and has at least one chat.
    """
    user_sub = "test-sub-123"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(f"/api/chats", params={"user_sub": user_sub})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # only check if list is non-empty
        assert "id" in data[0]
        assert "participant" in data[0]
        assert "first_name" in data[0]["participant"]
        assert "last_name" in data[0]["participant"]

@pytest.mark.asyncio
async def test_get_chats_user_with_no_chats():
    """
    Test retrieving chats for a user who exists but has no chats.
    Assumes user_sub="test-sub-nochats" exists in the DB but is not in any chat.
    """
    user_sub = "test-sub-nochats"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/chats", params={"user_sub": user_sub})

    assert response.status_code == 200
    data = response.json()
    assert data == []

@pytest.mark.asyncio
async def test_get_chats_missing_user_sub():
    """
    Test calling the endpoint without providing the required query parameter user_sub.
    Should return 422 Unprocessable Entity.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/chats")

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_chats_nonexistent_user():
    """
    Test retrieving chats for a user_sub that does not exist in the users table at all.
    Should return empty list, not error.
    """
    user_sub = "nonexistent-sub-xyz"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/chats", params={"user_sub": user_sub})

    assert response.status_code == 200
    data = response.json()
    assert data == []

@pytest.mark.asyncio
async def test_get_chats_user_with_multiple_chats():
    """
    Test user who is in multiple chats to ensure the endpoint returns all of them.
    Assumes that user_sub="test-sub-multi" is in >=2 chats.
    """
    user_sub = "test-sub-multi"

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/chats", params={"user_sub": user_sub})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for chat in data:
        assert "id" in chat
        assert "participant" in chat
        assert "first_name" in chat["participant"]
        assert "last_name" in chat["participant"]
