# tests/chat-service/test_post_media_messages.py

"""Integration tests for the /messages/media endpoint of chat-service.

These tests validate the behavior of the media-only message creation endpoint,
ensuring it correctly handles valid image uploads and various invalid cases.

Endpoint under test:
    POST /api/messages/media
"""

import pytest
import httpx
from pathlib import Path

# Base URL for chat-service (adjust if needed)
BASE_URL = "http://localhost:8000"

# Paths to test assets (relative to the tests/ directory)
ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEST_IMAGE_PATH = ASSETS_DIR / "test.jpg"
TEST_TEXT_PATH = ASSETS_DIR / "test.txt"


@pytest.mark.asyncio
async def test_message_with_only_media():
    """Test creating a valid media-only message.

    Sends a multipart/form-data request with a valid image file
    and required form fields (`chat_id`, `sender_sub`).

    Expected:
        - 200 OK
        - Response JSON includes `media_url` (not None)
        - `content` is None
    """
    data = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/messages/media", files=files)

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
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123")
    }

    # No media_file provided
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages/media", files=data)

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
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123")
    }

    with open(TEST_TEXT_PATH, "rb") as text_file:
        files = {
            **data,
            "media_file": (TEST_TEXT_PATH.name, text_file, "text/plain")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_nonexistent_chat_id_should_fail_media():
    """Test creating a media message with a non-existent chat_id.

    Expected:
        - 404 Not Found
    """
    data = {
        "chat_id": (None, "9999"),
        "sender_sub": (None, "test-sub-123")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_chat_id_should_fail_media():
    """Test creating a media message without chat_id.

    Expected:
        - 422 Unprocessable Entity
    """
    data = {
        "sender_sub": (None, "test-sub-123")
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            **data,
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 422
