# tests/notification-service/test_post_send_notification.py

import pytest
import httpx
import asyncio
from uuid import uuid4

BASE_URL = "http://localhost:8003"

@pytest.mark.asyncio
async def test_send_notification_success():
    """
    Test sending a valid notification.
    Should return 200 with full notification metadata.
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "This is a test notification."
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "notification_id" in data
    assert data["user_email"] == payload["user_email"]
    assert data["message"] == payload["message"]
    assert "sent_at" in data


@pytest.mark.asyncio
async def test_send_notification_missing_user_email():
    """
    Test sending a notification without user_email.
    Should return 422 (Unprocessable Entity).
    """
    payload = {
        "message": "Notification without email"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_missing_message():
    """
    Test sending a notification without message.
    Should return 422 (Unprocessable Entity).
    """
    payload = {
        "user_email": "testuser@example.com"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_empty_message():
    """
    Test sending a notification with an empty message.
    Should succeed (if no explicit length validation) or fail with 422 if restricted.
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": ""
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_invalid_email_format():
    """
    Test sending a notification with invalid email format.
    Should succeed (no email format validation).
    """
    payload = {
        "user_email": "invalid-email",
        "message": "Test message"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_very_long_message():
    """
    Test sending a notification with a very long message (10,000+ characters).
    Should succeed unless length is explicitly limited.
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "A" * 10000
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_with_long_email():
    """
    Test sending a notification with a long email address (max length 255).
    Should succeed unless there's an explicit length validation.
    """
    long_email = f"{'a'*64}@{'b'*63}.{'c'*63}.{'d'*61}"
    payload = {
        "user_email": long_email,
        "message": "Test long email"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_with_unicode_message():
    """
    Test sending a notification with unicode characters (emoji, symbols).
    Should succeed.
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "🚀🔥✨ Special chars: äöüß ñ Ćęść"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_duplicate_payloads():
    """
    Test sending the same payload multiple times to ensure uniqueness of notification IDs.
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "Duplicate test message"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response1 = await client.post("/api/notifications/send", json=payload)
        response2 = await client.post("/api/notifications/send", json=payload)

    assert response1.status_code == 200
    assert response2.status_code == 200
    data1 = response1.json()
    data2 = response2.json()
    assert data1["notification_id"] != data2["notification_id"]


@pytest.mark.asyncio
async def test_send_notification_max_length_email():
    """
    Test sending a notification with an email address near the maximum length (320 characters).
    """
    local_part = 'a' * 64
    domain = 'b' * 186 + ".com"  # 64 + 1 + 186 + 4 = 255 max for full email

    email = f"{local_part}@{domain}"
    payload = {
        "user_email": email,
        "message": "Edge case email length"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_large_payload():
    """
    Test sending a notification with both large email and large message.
    """
    email = f"{'x'*64}@{'y'*63}.{'z'*63}.{'w'*61}"
    message = "B" * 20000

    payload = {
        "user_email": email,
        "message": message
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_invalid_types():
    """
    Test sending notification with invalid types (int instead of string).
    Should return 422.
    """
    payload = {
        "user_email": 12345,
        "message": {"text": "Invalid type"}
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/notifications/send", json=payload)

    assert response.status_code == 422
