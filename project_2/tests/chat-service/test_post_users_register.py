# tests/chat-service/test_post_users_register.py

import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_register_user_success():
    """
    Test registering a new user with valid data.
    Should return 201 with success message.
    """
    payload = {
        "sub": f"test-sub-new-{uuid4()}",
        "email": f"newuser-{uuid4()}@example.com",
        "first_name": "Alice",
        "last_name": "Wonder"
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_register_user_already_exists():
    """
    Test registering a user that already exists.
    Should return 204 No Content.
    """
    payload = {
        "sub": "test-sub-new-2",
        "email": "newuser2@example.com",
        "first_name": "Bob",
        "last_name": "Builder"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # First registration
        await client.post("/api/users/register", json=payload)
        # Second registration (should hit "already exists")
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_register_user_missing_fields():
    """
    Test registering with missing required fields.
    Should return 422 Unprocessable Entity.
    """
    payload = {
        "sub": "test-sub-missing",
        "email": "missing@example.com",
        "first_name": "Missing"
        # last_name is missing
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_invalid_email():
    """
    Test registering with an invalid email format.
    Should return 422.
    """
    payload = {
        "sub": "test-sub-invalid-email",
        "email": "invalid-email",
        "first_name": "Invalid",
        "last_name": "Email"
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_empty_strings():
    """
    Test registering with empty string fields.
    Should succeed unless you have min_length validation.
    """
    payload = {
        "sub": f"test-sub-empty-{uuid4()}",
        "email": f"empty-{uuid4()}@example.com",
        "first_name": "",
        "last_name": ""
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_register_user_long_fields():
    """
    Test registering with very long field values.
    Should succeed unless length is restricted.
    """
    long_name = "A" * 255
    payload = {
        "sub": f"test-sub-long-{uuid4()}",
        "email": f"long-{uuid4()}@example.com",
        "first_name": long_name,
        "last_name": long_name
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_register_user_empty_payload():
    """
    Test registering with completely empty payload.
    Should return 422 Unprocessable Entity.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_with_extra_field():
    """
    Test registering with an extra field not defined in schema.
    Should succeed and ignore the extra field.
    """
    payload = {
        "sub": f"test-sub-extra-{uuid4()}",
        "email": f"extra-{uuid4()}@example.com",
        "first_name": "Extra",
        "last_name": "Field",
        "unexpected": "this should be ignored"
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/users/register", json=payload)

    assert response.status_code == 201
