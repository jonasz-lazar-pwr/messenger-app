# tests/chat-service/test_post_upload_media.py

import pytest
import httpx
from pathlib import Path

# Base URL for the media-service API
BASE_URL = "http://localhost:8002"

ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEST_IMAGE_PATH = ASSETS_DIR / "test.jpg"
TEST_TEXT_PATH = ASSETS_DIR / "test.txt"


@pytest.mark.asyncio
async def test_upload_image():
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
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/media/upload")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_unsupported_file_type():
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
    assert TEST_IMAGE_PATH.exists(), "Test image file does not exist"

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/media/upload", files=files)

    assert response.status_code == 200