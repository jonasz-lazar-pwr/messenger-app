# tests/chat-service/test_post_messages.py

import pytest
import httpx
from pathlib import Path

# Base URL for the chat-service API
BASE_URL = "http://localhost:8001"

# Użyj absolutnych ścieżek względem katalogu tests/
ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEST_IMAGE_PATH = ASSETS_DIR / "test.jpg"
TEST_TEXT_PATH = ASSETS_DIR / "test.txt"


@pytest.mark.asyncio
async def test_create_text_message():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "Test message content"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", data=data)

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["chat_id"] == int(data["chat_id"])
    assert data_out["sender_sub"] == data["sender_sub"]
    assert data_out["content"] == data["content"]


@pytest.mark.asyncio
async def test_message_empty_content_and_no_media():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": ""
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", data=data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_message_with_only_media():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123"
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/messages", data=data, files=files)

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["media_url"] is not None


@pytest.mark.asyncio
async def test_message_with_text_and_media():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "Here is a message with an image"
    }

    with open(TEST_IMAGE_PATH, "rb") as image_file:
        files = {
            "media_file": (TEST_IMAGE_PATH.name, image_file, "image/jpeg")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/messages", data=data, files=files)

    assert response.status_code == 200
    data_out = response.json()
    assert data_out["content"] == data["content"]
    assert data_out["media_url"] is not None


@pytest.mark.asyncio
async def test_message_missing_sender_sub():
    data = {
        "chat_id": 1,
        "content": "Message without sender_sub"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", data=data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_message_with_invalid_chat_id_type():
    data = {
        "chat_id": "one",
        "sender_sub": "test-sub-123",
        "content": "Invalid chat_id type"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", data=data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_message_with_very_long_content():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "A" * 10000
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("api/messages", data=data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_message_with_invalid_media_file_type():
    data = {
        "chat_id": 1,
        "sender_sub": "test-sub-123",
        "content": "Trying to send a text file as media"
    }

    with open(TEST_TEXT_PATH, "rb") as text_file:
        files = {
            "media_file": (TEST_TEXT_PATH.name, text_file, "text/plain")
        }
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            response = await client.post("api/messages", data=data, files=files)

    assert response.status_code == 400