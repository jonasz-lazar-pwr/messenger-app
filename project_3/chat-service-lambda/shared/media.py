# === shared/media.py ===
"""
Utilities for interacting with the media-service.

Includes:
- Uploading media files (images) to the media-service via HTTP.
- Parsing multipart/form-data from API Gateway proxy events.
"""

import os
import requests
from base64 import b64decode
from io import BytesIO
from typing import Tuple, Dict, Optional
from email.parser import BytesParser
from email.policy import EmailPolicy
from email.message import Message


def upload_to_media_service(file_field: Tuple[str, bytes, str]) -> dict[str, str]:
    """
    Upload a media file to the media-service and return metadata.

    Args:
        file_field (tuple): A tuple containing (filename, file content as bytes, MIME type).

    Returns:
        dict: A dictionary with:
            - 'url' (str): URL of the uploaded media.
            - 'id' (str): Unique ID of the media.

    Raises:
        Exception: If the upload fails or returns an invalid response.
    """
    media_host = os.environ["MEDIA_SERVICE_HOST"]
    upload_url = f"http://{media_host}/media/upload"

    files = {
        "file": (file_field[0], BytesIO(file_field[1]), file_field[2])
    }

    try:
        response = requests.post(
            upload_url,
            files=files,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Media upload rejected: {e.response.text}")
    except Exception as e:
        raise Exception(f"Failed to upload media: {str(e)}")


def parse_multipart_file(
    body_base64: str,
    content_type: str
) -> Tuple[Tuple[str, bytes, str], Dict[str, str]]:
    """
    Parse a multipart/form-data body from an API Gateway proxy event.

    Args:
        body_base64 (str): Base64-encoded body string from the event.
        content_type (str): Value of the Content-Type header, e.g.:
            'multipart/form-data; boundary=----WebKitFormBoundary...'.

    Returns:
        tuple:
            - file_field (tuple): A tuple of (filename, file_bytes, content_type).
            - fields (dict): A dictionary of additional form fields {name: value}.

    Raises:
        Exception: If the body cannot be parsed or no file part is found.
    """
    try:
        body_bytes = b64decode(body_base64)
        full_content = (
            f"Content-Type: {content_type}\r\n\r\n".encode() + body_bytes
        )

        msg: Message = BytesParser(policy=EmailPolicy()).parsebytes(full_content)

        if not msg.is_multipart():
            raise Exception("Provided content is not multipart")

        file_field: Optional[Tuple[str, bytes, str]] = None
        fields: Dict[str, str] = {}

        for part in msg.get_payload():
            disposition = part.get("Content-Disposition", "")
            if "form-data" not in disposition:
                continue

            name = part.get_param("name", header="Content-Disposition")
            filename = part.get_param("filename", header="Content-Disposition")

            if filename:
                file_bytes = part.get_payload(decode=True)
                file_type = part.get_content_type()
                file_field = (filename, file_bytes, file_type)
            elif name:
                value = part.get_content()
                fields[name] = value

        if file_field is None:
            raise Exception("No file uploaded in form-data")

        return file_field, fields

    except Exception as e:
        raise Exception(f"Failed to parse multipart/form-data: {str(e)}")
