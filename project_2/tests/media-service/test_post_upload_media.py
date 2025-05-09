# tests/chat-service/test_post_upload_media.py

"""
Integration tests for the /api/media/upload endpoint of media-service.

These tests validate the behavior of the media file upload endpoint,
including success cases, edge cases (large files, empty files),
and failure scenarios (unsupported types, missing files).

Endpoint under test:
    POST /api/media/upload
"""

import pytest
import httpx
from pathlib import Path
import io

# Base URL for the media-service API (adjust port if needed)
BASE_URL = "http://localhost:8000"

# Paths to test assets (relative to the tests/ directory)
ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEST_IMAGE_PATH = ASSETS_DIR / "test.jpg"
TEST_TEXT_PATH = ASSETS_DIR / "test.txt"


@pytest.mark.asyncio
async def test_upload_image():
    """
    Test uploading a valid image file.

    Expected:
        - 200 OK
        - JSON response includes 'id', 'filename', 'url'
        - 'filename' matches the uploaded file's name
    """
    assert TEST_IMAGE_PATH.exists(), "Test image file does not exist"

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/media/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "filename" in data
    assert "url" in data
    assert data["filename"] == TEST_IMAGE_PATH.name


@pytest.mark.asyncio
async def test_upload_missing_file():
    """
    Test uploading with no file provided (empty multipart/form-data).

    Expected:
        - 422 Unprocessable Entity (FastAPI validation error)
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/media/upload", files={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_unsupported_file_type():
    """
    Test uploading a file with an unsupported content type (e.g., text file).

    Expected:
        - 400 Bad Request (custom validation in API)
        - Alternatively, 415 Unsupported Media Type if enforced at lower level
    """
    assert TEST_TEXT_PATH.exists(), "Test text file does not exist"

    with open(TEST_TEXT_PATH, "rb") as text_file:
        files = {
            "file": (TEST_TEXT_PATH.name, text_file, "text/plain")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/media/upload", files=files)

    assert response.status_code in (400, 415)


@pytest.mark.asyncio
async def test_upload_large_image():
    """
    Test uploading a regular image file (simulates a larger payload, reuses test image).

    Expected:
        - 200 OK
    """
    assert TEST_IMAGE_PATH.exists(), "Test image file does not exist"

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/media/upload", files=files)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_really_large_image():
    """
    Test uploading a really large image file (simulated in-memory ~10MB).

    Expected:
        - 200 OK if server allows large uploads
        - 413 Payload Too Large if max size is enforced by API
    """
    big_file = io.BytesIO(b"\x00" * 10_000_000)  # 10 MB dummy data
    files = {
        "file": ("large_image.jpg", big_file, "image/jpeg")
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/media/upload", files=files)

    assert response.status_code in (200, 413)


@pytest.mark.asyncio
async def test_upload_empty_file():
    """
    Test uploading an empty image file (0 bytes).

    Expected:
        - 200 OK (if server accepts empty files)
    """
    empty_file = io.BytesIO(b"")
    files = {
        "file": ("empty.jpg", empty_file, "image/jpeg")
    }
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/media/upload", files=files)

    assert response.status_code == 200
