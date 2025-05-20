# api/routes/media.py

"""
Media upload endpoint.

This module defines routes for handling media file uploads,
including S3 upload and metadata persistence in DynamoDB.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from api.services.s3 import upload_file_to_s3
from api.services.dynamo import save_media_metadata
from api.schemas.media import MediaUploadResponse

# Create router instance for media routes
router = APIRouter()


@router.post(
    "/upload/",
    response_model=MediaUploadResponse,
    summary="Upload a media file",
    description=(
        "Uploads an image file to S3 and stores associated metadata in DynamoDB. "
        "Returns the media ID and URL."
    ),
    responses={
        200: {"description": "Media uploaded successfully"},
        400: {"description": "Invalid input – only image files are allowed"},
        500: {"description": "Failed to store metadata"}
    },
    tags=["Media"]
)
async def upload_media(file: UploadFile = File(...)):
    """
    Handle media upload request.

    Steps:
    - Validates that the uploaded file is an image (content-type starts with 'image/').
    - Uploads the file to S3 and retrieves the media ID, S3 key, and URL.
    - Persists metadata to DynamoDB for future reference.

    Args:
        file (UploadFile): The image file sent by the client.

    Returns:
        MediaUploadResponse: Contains the media UUID, original filename, and public URL.

    Raises:
        HTTPException: 400 if the file is not an image.
        HTTPException: 500 if the upload or metadata storage fails.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # Upload file to S3
    try:
        media_id, s3_key, media_url = await upload_file_to_s3(
            file,
            filename=file.filename,
            content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")

    # Save metadata to DynamoDB
    try:
        await save_media_metadata(
            media_id=media_id,
            filename=file.filename,
            s3_key=s3_key,
            content_type=file.content_type,
            media_url=media_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save metadata to DynamoDB: {str(e)}"
        )

    return MediaUploadResponse(
        id=media_id,
        filename=file.filename,
        url=media_url
    )