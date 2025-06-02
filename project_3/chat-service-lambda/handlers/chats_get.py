# === handlers/chats_get.py ===
"""
Retrieve all chats of the authenticated user.

This AWS Lambda function returns a list of chat entries where the authenticated
user is a participant. For each chat, it includes the chat ID and basic
information about the other participant.

Triggered by:
    GET /api/chats

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

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models import Chat, User
from shared.schemas.chat import ChatListItem, ChatParticipant
from shared.utils import build_response

# Initialize Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """
    Lambda handler for retrieving all chats of the authenticated user.

    Args:
        event (dict): API Gateway event with JWT token in headers.
        context (LambdaContext): Lambda runtime context (unused).

    Returns:
        dict: API Gateway-compatible HTTP response containing chat list.
    """
    try:
        user_sub = get_current_user_sub(event)
    except Exception as e:
        return build_response(HTTPStatus.UNAUTHORIZED, {"error": str(e)})

    try:
        with sync_session() as session:
            chats = session.execute(
                select(Chat).where(
                    (Chat.user1_sub == user_sub) | (Chat.user2_sub == user_sub)
                )
            ).scalars().all()

            chat_items = []

            for chat in chats:
                other_sub = chat.user2_sub if chat.user1_sub == user_sub else chat.user1_sub

                other_user = session.execute(
                    select(User).where(User.sub == other_sub)
                ).scalar_one_or_none()

                if not other_user:
                    continue

                item = ChatListItem(
                    id=chat.id,
                    participant=ChatParticipant(
                        first_name=other_user.first_name,
                        last_name=other_user.last_name,
                    ),
                )
                chat_items.append(item.model_dump())

            return build_response(HTTPStatus.OK, chat_items)

    except Exception as e:
        return build_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"Internal error: {str(e)}"})
