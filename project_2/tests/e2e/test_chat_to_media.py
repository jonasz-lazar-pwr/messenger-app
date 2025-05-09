# tests/e2e/test_chat_to_media.py

"""E2E tests: chat-service -> media-service integration.

This verifies that uploading media via chat-service:
- saves the file to S3,
- stores metadata in DynamoDB,
- and handles edge cases (missing/invalid files).
"""

import pytest
import httpx
import boto3
import asyncio
import io

# Chat-service base URL
CHAT_BASE_URL = "http://localhost:8000"

# Localstack config (S3 + DynamoDB emulation)
LOCALSTACK_URL = "http://localhost:4566"
S3_BUCKET_NAME = "media-files"
MEDIA_TABLE = "MediaMetadata"

# S3 client
S3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_URL,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)

# DynamoDB client
DYNAMODB = boto3.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_URL,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)


@pytest.mark.asyncio
async def test_chat_media_upload_and_verify_s3_and_dynamo():
    """
    E2E: Upload a valid image via chat-service and verify:
    - media_url and media_id in response,
    - file exists in S3,
    - metadata exists in DynamoDB.
    """
    # Prepare dummy image file
    file_content = b"fake-image-bytes"
    file_name = "e2e_test_image.jpg"

    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "media_file": (file_name, file_content, "image/jpeg")
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 200, response.text
    data = response.json()

    # Validate response fields
    assert "media_url" in data and data["media_url"]
    assert "media_id" in data and data["media_id"]
    assert data["content"] is None

    media_url = data["media_url"]
    media_id = data["media_id"]

    # Wait for S3/Dynamo propagation
    await asyncio.sleep(0.1)

    # --- Check S3 ---
    s3_key = media_url.split(f"{S3_BUCKET_NAME}/")[-1]
    s3_objects = S3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    all_keys = [obj["Key"] for obj in s3_objects.get("Contents", [])]
    assert s3_key in all_keys, f"S3 missing expected key: {s3_key}"

    # --- Check DynamoDB ---
    table = DYNAMODB.Table(MEDIA_TABLE)
    response = table.get_item(Key={"id": media_id})
    item = response.get("Item")
    assert item, "Media metadata missing in DynamoDB"
    assert item["id"] == media_id
    assert item["filename"] == file_name
    assert item["url"] == media_url


@pytest.mark.asyncio
async def test_chat_media_upload_missing_file_should_fail():
    """
    E2E: Upload media message without providing media_file.
    Expect 422 Unprocessable Entity from FastAPI validation.
    """
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123")
        # no media_file
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_media_upload_invalid_file_type_should_fail():
    """
    E2E: Upload invalid file type (not image/*).
    Expect 400 Bad Request from chat-service.
    """
    fake_text_file = io.BytesIO(b"Hello world from txt")
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "media_file": ("fake.txt", fake_text_file, "text/plain")
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 400
    assert "Only image files are allowed" in response.text


@pytest.mark.asyncio
async def test_chat_media_upload_missing_chat_id_should_fail():
    """
    E2E: Upload file without chat_id. Should fail with 422.
    """
    file_content = b"valid-image"
    files = {
        "sender_sub": (None, "test-sub-123"),
        "media_file": ("no_chat.jpg", file_content, "image/jpeg")
    }

    async with httpx.AsyncClient(base_url=CHAT_BASE_URL) as client:
        response = await client.post("/api/messages/media", files=files)

    assert response.status_code == 422