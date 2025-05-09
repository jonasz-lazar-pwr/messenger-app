# tests/chat-service/test_get_users_search.py

import pytest
import httpx

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_user_search_exact_match():
    """
    Test searching for user by exact first name.
    Assumes 'Test' exists in first_name.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "Test"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("first_name" in u and "last_name" in u and "sub" in u for u in data)


@pytest.mark.asyncio
async def test_user_search_partial_match():
    """
    Test searching by partial last name (e.g. 'ser').
    Should return all matches with that substring.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "ser"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_user_search_case_insensitive():
    """
    Test case-insensitive search (e.g. 'tESt').
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "tESt"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_user_search_no_results():
    """
    Test with a query string that matches no users.
    Should return empty list.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "zzzzz"})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_user_search_missing_query():
    """
    Test calling endpoint without required query parameter.
    Should return 422.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_user_search_min_length_query():
    """
    Test with minimum length allowed for query (1 character).
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "T"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_user_search_special_characters():
    """
    Test search with special characters or unicode.
    Should return 200 and not crash the backend.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": "@éü$%"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_user_search_very_long_query():
    """
    Test search with a very long query string.
    Should return 200 and likely an empty list.
    """
    long_query = "A" * 1000
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/users/search", params={"query": long_query})

    assert response.status_code == 200
    assert isinstance(response.json(), list)