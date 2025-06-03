# === handlers/messages_post_text.py ===
"""
Send a plain text message in a chat.

This AWS Lambda function creates a new text message in a chat where
the authenticated user is a participant. It verifies the JWT token,
validates input, and saves the message in the database.

The function also publishes a notification event to Amazon SQS for
the notification-service to consume asynchronously.

Triggered by:
    POST /api/messages/text

Required environment variables:
    - COGNITO_POOL_ID
    - COGNITO_CLIENT_ID
    - COGNITO_ISSUER_URL
    - PSQL_USER
    - PSQL_PASSWORD
    - PSQL_HOST
    - PSQL_PORT
    - PSQL_NAME
    - NOTIFICATION_RECEIVER_EMAIL
"""

from http import HTTPStatus
from sqlalchemy import select
from pydantic import ValidationError

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models.chat import Chat
from shared.models.message import Message
from shared.schemas.message import MessageTextIn, MessageOut
from shared.sqs import notify_about_message
from shared.utils import build_response, parse_body

# Configure Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """Handle POST /api/messages/text request.

    This handler authenticates the user, validates input,
    checks access to the chat, saves a text message to the database,
    and publishes a notification event to SQS.

    Args:
        event (dict): API Gateway proxy event with headers and body.
        context (LambdaContext): AWS Lambda context object (unused).

    Returns:
        dict: API Gateway-compatible JSON response.
    """
    try:
        sender_sub = get_current_user_sub(event)

        try:
            body = parse_body(event)
            message_in = MessageTextIn.model_validate(body)
        except (ValidationError, ValueError) as exc:
            return build_response(
                HTTPStatus.BAD_REQUEST, {"detail": str(exc)}
            )

        with sync_session() as db:
            chat = db.execute(
                select(Chat).where(Chat.id == message_in.chat_id)
            ).scalar_one_or_none()

            if chat is None:
                return build_response(
                    HTTPStatus.NOT_FOUND, {"detail": "Chat not found"}
                )

            if sender_sub not in [chat.user1_sub, chat.user2_sub]:
                return build_response(
                    HTTPStatus.FORBIDDEN,
                    {"detail": "You are not a participant of this chat"},
                )

            message = Message(
                chat_id=message_in.chat_id,
                sender_sub=sender_sub,
                content=message_in.content,
                media_url=None,
                media_id=None,
            )
            db.add(message)
            db.commit()
            db.refresh(message)

            notify_about_message(
                db=db,
                sender_sub=sender_sub,
                message_text=message.content,
                has_media=False,
            )

            message_out = MessageOut.model_validate(message).model_dump(
                mode="json"
            )
            return build_response(HTTPStatus.OK, message_out)

    except Exception as exc:
        return build_response(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {"detail": str(exc)}
        )
