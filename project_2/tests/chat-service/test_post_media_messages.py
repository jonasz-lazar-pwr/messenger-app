# tests/chat-service/test_post_media_messages.py

import pytest
import httpx
from pathlib import Path
import json

# Base URL for chat-service
BASE_URL = "http://localhost:8001"

# Paths to test assets (relative to the tests/ directory)
ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEST_IMAGE_PATH = ASSETS_DIR / "test.jpg"
TEST_TEXT_PATH = ASSETS_DIR / "test.txt"

# Mock JWT payload (same across tests)
X_USER_PAYLOAD = json.dumps({"sub": "test-sub-123"})


@pytest.mark.asyncio
async def test_message_with_only_media():
    """Test creating a valid media-only message.

    Sends a multipart/form-data request with a valid image file
    and required form field (`chat_id`). The sender is provided
    via the X-User-Payload header.

    Expected:
        - 200 OK
        - Response JSON includes `media_url` (not None)
        - `content` is None
    """
    data = {
        "chat_id": (None, "1")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post(
                "/messages/media",
                files=files,
                headers={"X-User-Payload": X_USER_PAYLOAD}
            )

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["media_url"] is not None
    assert data_out["content"] is None


@pytest.mark.asyncio
async def test_missing_media_file_should_fail():
    """Test creating a media message without providing a file.

    Sends a multipart/form-data request with form fields but no file.
    The API should reject the request as invalid.

    Expected:
        - 422 Unprocessable Entity (missing required file)
    """
    data = {
        "chat_id": (None, "1")
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/messages/media",
            files=data,
            headers={"X-User-Payload": X_USER_PAYLOAD}
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_media_file_type_should_fail():
    """Test creating a media message with an invalid file type.

    Sends a multipart/form-data request with a text file
    instead of a valid image file. The API should reject it.

    Expected:
        - 400 Bad Request (invalid media type)
    """
    data = {
        "chat_id": (None, "1")
    }

    with open(TEST_TEXT_PATH, "rb") as text_file:
        files = {
            **data,
            "media_file": (TEST_TEXT_PATH.name, text_file, "text/plain")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post(
                "/messages/media",
                files=files,
                headers={"X-User-Payload": X_USER_PAYLOAD}
            )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_nonexistent_chat_id_should_fail_media():
    """Test creating a media message with a non-existent chat_id.

    Expected:
        - 404 Not Found
    """
    data = {
        "chat_id": (None, "9999")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post(
                "/messages/media",
                files=files,
                headers={"X-User-Payload": X_USER_PAYLOAD}
            )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_chat_id_should_fail_media():
    """Test creating a media message without chat_id.

    Expected:
        - 422 Unprocessable Entity
    """
    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post(
                "/messages/media",
                files=files,
                headers={"X-User-Payload": X_USER_PAYLOAD}
            )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_token_header_should_fail():
    """Test creating a media message without the X-User-Payload header.

    Expected:
        - 422 Unprocessable Entity (missing header)
    """
    data = {
        "chat_id": (None, "1")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post(
                "/messages/media",
                files=files
                # Note: No X-User-Payload header!
            )

    assert response.status_code == 422
