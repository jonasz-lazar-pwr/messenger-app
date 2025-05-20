# api/services/media.py

"""
Media service integration module.

This module provides a utility function to upload media files (e.g., images)
to the media-service, which is responsible for handling storage (e.g., S3).

The service:
- Accepts an `UploadFile` object.
- Sends the file to the media-service via HTTP POST.
- Parses and returns the response metadata (file URL and unique ID).

Raises appropriate HTTPException errors in case of failures.
"""

import httpx
from fastapi import HTTPException, UploadFile
from api.core.config import settings


async def upload_media_to_s3(media_file: UploadFile) -> dict:
    """
    Upload a media file to the media-service and return metadata.

    This function:
    1. Builds a multipart/form-data request using the `UploadFile`.
    2. Sends the file to the media-service `/media/upload` endpoint.
    3. Parses the JSON response to extract the `url` and `id` of the uploaded file.

    Args:
        media_file (UploadFile): The media file to be uploaded. Must include
            filename, content, and content type.

    Returns:
        dict: A dictionary with the following keys:
            - 'url' (str): The accessible URL of the uploaded file.
            - 'id' (str): The unique identifier of the uploaded file.

    Raises:
        HTTPException:
            - 400: If the media-service rejects the upload (e.g., invalid file type).
            - 500: If any unexpected error occurs during upload (e.g., connection issues).
    """
    form_data = {
        "file": (media_file.filename, media_file.file, media_file.content_type)
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"http://{settings.MEDIA_SERVICE_HOST}:{settings.MEDIA_SERVICE_PORT}/media/upload/",
                files=form_data
            )
        response.raise_for_status()
        media_response = response.json()
        return {
            "url": media_response["url"],
            "id": media_response["id"]
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Media upload rejected: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload media: {str(e)}")