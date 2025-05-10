# tests/chat-service/test_post_users_register.py

import pytest
import httpx
import json
from uuid import uuid4

BASE_URL = "http://localhost:8001"


@pytest.mark.asyncio
async def test_register_user_success():
    """
    Test registering a new user with valid data.
    Should return 201 with success message.
    """
    payload = {
        "sub": f"test-sub-new-{uuid4()}",
        "email": f"newuser-{uuid4()}@example.com",
        "given_name": "Alice",
        "family_name": "Wonder"
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

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
        "sub": f"test-sub-existing-{uuid4()}",
        "email": f"existing-{uuid4()}@example.com",
        "given_name": "Bob",
        "family_name": "Builder"
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # First registration
        await client.post("/users/register", headers=headers)
        # Second registration (should hit "already exists")
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_register_user_missing_fields():
    """
    Test registering with missing required fields in X-User-Payload.
    Should return 400 Bad Request.
    """
    payload = {
        "sub": f"test-sub-missing-{uuid4()}",
        "email": f"missing-{uuid4()}@example.com",
        # 'given_name' is missing
        "family_name": "Missing"
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Missing required user attributes in token payload"


@pytest.mark.asyncio
async def test_register_user_invalid_json_in_header():
    """
    Test registering with invalid JSON in X-User-Payload header.
    Should return 400 Bad Request.
    """
    headers = {
        "X-User-Payload": "not-a-json-string"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid JSON in X-User-Payload header"


@pytest.mark.asyncio
async def test_register_user_missing_header():
    """
    Test registering without the X-User-Payload header.
    Should return 422 Unprocessable Entity (missing header).
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_empty_strings():
    """
    Test registering a user where required fields are present but empty strings.
    Should return 400 Bad Request.
    """
    payload = {
        "sub": f"test-sub-empty-{uuid4()}",
        "email": f"empty-{uuid4()}@example.com",
        "given_name": "",
        "family_name": ""
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Missing required user attributes in token payload"


@pytest.mark.asyncio
async def test_register_user_very_long_fields():
    """
    Test registering with very long strings in the payload.
    Should succeed unless you have length restrictions.
    """
    long_name = "A" * 500
    payload = {
        "sub": f"test-sub-long-{uuid4()}",
        "email": f"long-{uuid4()}@example.com",
        "given_name": long_name,
        "family_name": long_name
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_register_user_with_extra_fields():
    """
    Test registering with extra fields in the payload.
    Should succeed and ignore extra fields.
    """
    payload = {
        "sub": f"test-sub-extra-{uuid4()}",
        "email": f"extra-{uuid4()}@example.com",
        "given_name": "Extra",
        "family_name": "Field",
        "unexpected": "some-extra-value",
        "role": "admin"  # simulating extra claim
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"


@pytest.mark.asyncio
async def test_register_user_missing_sub():
    """
    Test registering without 'sub' field in the payload.
    Should return 400 Bad Request.
    """
    payload = {
        "email": f"nosub-{uuid4()}@example.com",
        "given_name": "NoSub",
        "family_name": "User"
    }
    headers = {
        "X-User-Payload": json.dumps(payload)
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/register", headers=headers)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Missing required user attributes in token payload"
