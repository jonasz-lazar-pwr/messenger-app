# === handlers/messages_post_media.py ===
"""
Send a media message in a chat.

This AWS Lambda function handles multipart/form-data containing a media file.
It uploads the file to media-service, validates the chat and user, saves the
message in the database, and publishes a notification event to SQS.

Triggered by:
    POST /api/messages/media

Required environment variables:
    - PSQL_HOST
    - PSQL_PORT
    - PSQL_USER
    - PSQL_PASSWORD
    - PSQL_NAME
    - COGNITO_POOL_ID
    - COGNITO_CLIENT_ID
    - COGNITO_ISSUER_URL
    - MEDIA_SERVICE_HOST
    - AWS_SQS_NOTIFICATION_QUEUE_URL
    - NOTIFICATION_RECEIVER_EMAIL
"""

from http import HTTPStatus
from uuid import UUID
from sqlalchemy import select

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models.chat import Chat
from shared.models.message import Message
from shared.schemas.message import MessageOut
from shared.utils import build_response
from shared.media import parse_multipart_file, upload_to_media_service
from shared.sqs import notify_about_message

# Configure Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """Handle POST /api/messages/media request.

    This handler processes a multipart/form-data request with a media file.
    It uploads the file, verifies the user and chat, stores the message in
    the database, and publishes a notification event to SQS.

    Args:
        event (dict): API Gateway proxy event.
        context (LambdaContext): AWS Lambda context object (unused).

    Returns:
        dict: API Gateway-compatible JSON response.
    """
    try:
        sender_sub = get_current_user_sub(event)

        content_type = (
            event["headers"].get("Content-Type")
            or event["headers"].get("content-type")
        )
        if not content_type:
            return build_response(
                HTTPStatus.BAD_REQUEST,
                {"detail": "Missing Content-Type header"},
            )

        try:
            file_field, fields = parse_multipart_file(event["body"], content_type)
            chat_id = int(fields.get("chat_id"))
        except Exception as exc:
            return build_response(
                HTTPStatus.BAD_REQUEST,
                {"detail": f"Malformed multipart data: {str(exc)}"},
            )

        with sync_session() as db:
            chat = db.execute(select(Chat).where(Chat.id == chat_id)).scalar_one_or_none()

            if chat is None:
                return build_response(
                    HTTPStatus.NOT_FOUND,
                    {"detail": "Chat not found"},
                )

            if sender_sub not in [chat.user1_sub, chat.user2_sub]:
                return build_response(
                    HTTPStatus.FORBIDDEN,
                    {"detail": "You are not a participant of this chat"},
                )

            try:
                metadata = upload_to_media_service(file_field)
            except Exception as exc:
                return build_response(
                    HTTPStatus.BAD_REQUEST, {"detail": str(exc)}
                )

            message = Message(
                chat_id=chat_id,
                sender_sub=sender_sub,
                content=None,
                media_url=metadata["url"],
                media_id=UUID(metadata["id"]),
            )
            db.add(message)
            db.commit()
            db.refresh(message)

            notify_about_message(
                db=db,
                sender_sub=sender_sub,
                message_text=None,
                has_media=True,
            )

            message_out = MessageOut.model_validate(message).model_dump(mode="json")
            return build_response(HTTPStatus.OK, message_out)

    except Exception as exc:
        return build_response(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {"detail": str(exc)},
        )
