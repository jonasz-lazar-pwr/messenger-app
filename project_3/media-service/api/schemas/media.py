# api/schemas/media.py

from pydantic import BaseModel, Field


class MediaUploadResponse(BaseModel):
    """
    Response schema returned after a successful media file upload.

    This schema contains basic information about the uploaded file,
    such as its generated ID, original filename, and the URL pointing to it in S3.
    """
    id: str = Field(..., description="Unique ID of the uploaded media (UUID as string)")
    filename: str = Field(..., description="Original name of the uploaded file")
    url: str = Field(..., description="Publicly accessible URL to the uploaded media")
