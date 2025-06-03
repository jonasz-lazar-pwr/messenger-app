# === handlers/chats_post.py ===
"""
Create a one-on-one chat between the current user and a target user.

Triggered by:
    POST /api/chats

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
from sqlalchemy import select, or_

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models import User, Chat
from shared.schemas.chat import ChatCreate, ChatParticipant, ChatListItem
from shared.utils import build_response, parse_body

# Initialize Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """
    Lambda handler for creating a new one-on-one chat.

    Args:
        event (dict): API Gateway event with JWT and request body.
        context (LambdaContext): Lambda runtime context (unused).

    Returns:
        dict: API Gateway-compatible HTTP response with chat info or error.
    """
    try:
        user_sub = get_current_user_sub(event)
    except Exception as e:
        return build_response(HTTPStatus.UNAUTHORIZED, {"error": str(e)})

    try:
        data = parse_body(event)
        chat_in = ChatCreate(**data)
    except Exception:
        return build_response(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON or missing fields"})

    if user_sub == chat_in.target_user_sub:
        return build_response(HTTPStatus.BAD_REQUEST, {"error": "Cannot create a chat with yourself"})

    try:
        with sync_session() as db:
            target_user = db.execute(
                select(User).where(User.sub == chat_in.target_user_sub)
            ).scalar_one_or_none()

            if not target_user:
                return build_response(HTTPStatus.NOT_FOUND, {"error": "Target user not found"})

            existing_chat = db.execute(
                select(Chat).where(
                    or_(
                        (Chat.user1_sub == user_sub) & (Chat.user2_sub == chat_in.target_user_sub),
                        (Chat.user1_sub == chat_in.target_user_sub) & (Chat.user2_sub == user_sub)
                    )
                )
            ).scalar_one_or_none()

            if existing_chat:
                return build_response(HTTPStatus.CONFLICT, {"error": "Chat already exists"})

            new_chat = Chat(user1_sub=user_sub, user2_sub=chat_in.target_user_sub)
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            db.refresh(new_chat, attribute_names=["user1", "user2"])

            other_user = new_chat.user2 if new_chat.user1_sub == user_sub else new_chat.user1

            response_data = ChatListItem(
                id=new_chat.id,
                participant=ChatParticipant(
                    first_name=other_user.first_name,
                    last_name=other_user.last_name
                )
            )
            return build_response(HTTPStatus.OK, response_data.model_dump())

    except Exception as e:
        return build_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
