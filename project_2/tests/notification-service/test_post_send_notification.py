# tests/notification-service/test_post_send_notification.py

import pytest
import httpx
from dateutil.parser import parse

# Base URL for the notification-service API
BASE_URL = "http://localhost:8003"


@pytest.mark.asyncio
async def test_send_notification_success():
    """
    Test sending a valid notification.

    Expected:
        - 200 OK
        - JSON response includes: 'notification_id', 'user_email', 'message', 'sent_at'
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "This is a test notification."
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "notification_id" in data
    assert data["user_email"] == payload["user_email"]
    assert data["message"] == payload["message"]
    assert "sent_at" in data


@pytest.mark.asyncio
async def test_send_notification_missing_user_email():
    """
    Test sending a notification without 'user_email'.

    Expected:
        - 422 Unprocessable Entity (validation error)
    """
    payload = {
        "message": "Notification without email"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_missing_message():
    """
    Test sending a notification without 'message'.

    Expected:
        - 422 Unprocessable Entity (validation error)
    """
    payload = {
        "user_email": "testuser@example.com"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_empty_message():
    """
    Test sending a notification with an empty message.

    Expected:
        - 422 Unprocessable Entity (because of min_length=1 constraint)
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": ""
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_invalid_email_format():
    """
    Test sending a notification with invalid email format.

    Expected:
        - 422 Unprocessable Entity (because of EmailStr field validation)
    """
    payload = {
        "user_email": "invalid-email",
        "message": "Test message"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_very_long_message():
    """
    Test sending a notification with a very long message (10,000+ characters).

    Expected:
        - 200 OK (unless length limit is enforced)
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "A" * 10000
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_with_long_email():
    """
    Test sending a notification with a long email address (close to max length 255).

    Expected:
        - 200 OK (if within allowed limit and valid format)
    """
    long_email = f"{'a'*64}@{'b'*63}.{'c'*63}.{'d'*61}"
    payload = {
        "user_email": long_email,
        "message": "Test long email"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_with_unicode_message():
    """
    Test sending a notification with unicode characters (emoji, accents).

    Expected:
        - 200 OK
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "🚀🔥✨ Special chars: äöüß ñ Ćęść"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_duplicate_payloads():
    """
    Test sending the same payload multiple times to ensure unique notification IDs.

    Expected:
        - 200 OK both times
        - Different 'notification_id' in each response
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "Duplicate test message"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response1 = await client.post("/notifications/send", json=payload)
        response2 = await client.post("/notifications/send", json=payload)

    assert response1.status_code == 200
    assert response2.status_code == 200
    data1 = response1.json()
    data2 = response2.json()
    assert data1["notification_id"] != data2["notification_id"]


@pytest.mark.asyncio
async def test_send_notification_max_length_email():
    """
    Test sending a notification with an email at/near 320 characters (max allowed by spec).

    Expected:
        - 422 Unprocessable Entity (should fail EmailStr validation)
    """
    local_part = 'a' * 64
    domain = 'b' * 186 + ".com"  # ~255 chars full domain

    email = f"{local_part}@{domain}"
    payload = {
        "user_email": email,
        "message": "Edge case email length"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_large_payload():
    """
    Test sending a notification with both large email and large message.

    Expected:
        - 200 OK (if valid and within size limits)
    """
    email = f"{'x'*64}@{'y'*63}.{'z'*63}.{'w'*61}"
    message = "B" * 20000

    payload = {
        "user_email": email,
        "message": message
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_notification_invalid_types():
    """
    Test sending notification with invalid types (int instead of string).

    Expected:
        - 422 Unprocessable Entity
    """
    payload = {
        "user_email": 12345,  # should be string (email)
        "message": {"text": "Invalid type"}  # should be string
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_notification_sent_at_is_timestamp():
    """
    Test that the 'sent_at' field in the response is a valid ISO timestamp.

    Expected:
        - 200 OK
        - sent_at can be parsed to datetime without error
    """
    payload = {
        "user_email": "testuser@example.com",
        "message": "Timestamp test"
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/notifications/send", json=payload)

    assert response.status_code == 200
    data = response.json()
    # Validate that sent_at is a valid timestamp
    try:
        parsed_date = parse(data["sent_at"])
        assert parsed_date is not None
    except Exception:
        pytest.fail("sent_at is not a valid timestamp")