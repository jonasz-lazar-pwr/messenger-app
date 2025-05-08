# tests/e2e/test_chat_with_media.py

"""End-to-end test for media upload via chat-service and verification in S3 and DynamoDB.

This module tests the complete flow of uploading media through chat-service,
checking if the file is stored in S3 and metadata is saved in DynamoDB.
"""

import pytest
import httpx
import boto3
import asyncio

BASE_URL = "http://localhost:8001"
LOCALSTACK_URL = "http://localhost:4566"

# S3 setup (for checking uploaded files)
S3 = boto3.client(
    "s3",
    endpoint_url=LOCALSTACK_URL,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)

S3_BUCKET_NAME = "media-files"

# DynamoDB setup (for checking media metadata)
DYNAMODB = boto3.resource(
    "dynamodb",
    endpoint_url=LOCALSTACK_URL,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    aws_session_token="test"
)

MEDIA_TABLE = "MediaMetadata"


@pytest.mark.asyncio
async def test_upload_media_via_chat_service_and_verify_in_s3_and_dynamodb():
    """Upload media via chat-service and verify in S3 bucket and DynamoDB metadata table."""
    # Prepare file content and metadata
    file_content = b"Test file content for E2E test"
    file_name = "test_e2e_upload.jpg"

    # Prepare form data for chat-service
    data = {
        "chat_id": "1",
        "sender_sub": "test-sub-123",
        "content": "Testing E2E media upload"
    }
    files = {
        "media_file": (file_name, file_content, "image/jpeg")
    }

    # Send POST request to chat-service
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data, files=files)

    # Verify HTTP response and extract media info
    assert response.status_code == 200
    message_data = response.json()
    print("Response:", message_data)

    assert "media_url" in message_data and message_data["media_url"]
    assert "media_id" in message_data and message_data["media_id"]

    media_url = message_data["media_url"]
    media_id = message_data["media_id"]

    # Wait briefly for propagation to S3 and DynamoDB
    await asyncio.sleep(0.5)

    # Verify the file exists in S3
    s3_key = media_url.split(f"{S3_BUCKET_NAME}/")[-1]
    s3_objects = S3.list_objects_v2(Bucket=S3_BUCKET_NAME)
    all_keys = [obj["Key"] for obj in s3_objects.get("Contents", [])]

    assert s3_key in all_keys, f"File {s3_key} not found in S3 bucket {S3_BUCKET_NAME}"

    # Verify the metadata exists in DynamoDB
    table = DYNAMODB.Table(MEDIA_TABLE)
    response = table.get_item(Key={"id": media_id})
    item = response.get("Item")

    assert item, "Media metadata not found in DynamoDB"
    assert item["id"] == media_id
    assert item["filename"] == file_name
    assert item["url"] == media_url


@pytest.mark.asyncio
async def test_create_message_without_text_or_media():
    """Test sending a message without text and without media; expect 400 Bad Request."""
    data = {
        "chat_id": "1",
        "sender_sub": "test-sub-123"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", data=data)

    assert response.status_code == 400
    assert "Message must contain text or a media file" in response.text


@pytest.mark.asyncio
async def test_create_message_with_invalid_file_type():
    """Test uploading an invalid file type; expect 400 Bad Request from media-service."""
    files = {
        "chat_id": (None, "1"),
        "sender_sub": (None, "test-sub-123"),
        "content": (None, "Trying to upload invalid file"),
        "media_file": ("malware.exe", b"fake exe content", "application/octet-stream")
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/messages", files=files)

    # Expecting a 400 Bad Request from the media-service due to invalid file type
    assert response.status_code == 400
    assert "Only image files are allowed" in response.text