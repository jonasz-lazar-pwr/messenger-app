# === handlers/messages_get_by_chat.py ===
"""
Retrieve messages from a given chat if the user is a participant.

This AWS Lambda function validates the user's JWT token and returns all messages
from a specified chat ID, ordered by timestamp.

Triggered by:
    GET /api/messages/{chat_id}

Required environment variables:
    - COGNITO_POOL_ID
    - COGNITO_CLIENT_ID
    - COGNITO_ISSUER_URL
    - PSQL_USER
    - PSQL_PASSWORD
    - PSQL_HOST
    - PSQL_PORT
    - PSQL_NAME
"""

from http import HTTPStatus
from sqlalchemy import select
from pydantic import TypeAdapter

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models import Chat, Message
from shared.schemas.message import MessageOut
from shared.utils import build_response

# Init Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """
    Lambda handler for retrieving messages from a chat.

    This function validates JWT and returns all messages from a specified
    chat if the user is a participant.

    Args:
        event (dict): API Gateway event including pathParameters and headers.
        context (LambdaContext): AWS Lambda context (unused).

    Returns:
        dict: API Gateway-compatible HTTP response with message list or error.
    """
    try:
        chat_id = int(event["pathParameters"]["chat_id"])
    except Exception:
        return build_response(HTTPStatus.BAD_REQUEST, {"error": "Invalid or missing chat_id"})

    try:
        user_sub = get_current_user_sub(event)
    except Exception as e:
        return build_response(HTTPStatus.UNAUTHORIZED, {"error": str(e)})

    try:
        with sync_session() as session:
            chat = session.execute(select(Chat).where(Chat.id == chat_id)).scalar_one_or_none()

            if not chat:
                return build_response(HTTPStatus.NOT_FOUND, {"error": "Chat not found"})

            if user_sub not in [chat.user1_sub, chat.user2_sub]:
                return build_response(HTTPStatus.FORBIDDEN, {"error": "Access denied"})

            db_messages = session.execute(
                select(Message).where(Message.chat_id == chat_id).order_by(Message.sent_at)
            ).scalars().all()

            messages = [MessageOut.model_validate(m) for m in db_messages]
            json_body = TypeAdapter(list[MessageOut]).dump_json(messages)

            return {
                "statusCode": HTTPStatus.OK,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH"
                },
                "body": json_body
            }

    except Exception as e:
        return build_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
