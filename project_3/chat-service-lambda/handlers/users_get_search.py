# === handlers/users_get_search.py ===
"""
Search users by name, excluding the current user and existing chat partners.

This AWS Lambda function enables the authenticated user to search for other users
by first or last name (case-insensitive). The search excludes:
- the current authenticated user,
- users who already have an existing chat with them.

Triggered by:
    GET /api/users/search

Authorization:
    Requires a valid JWT token in the Authorization header (Bearer).

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
from sqlalchemy import select, or_, exists
from pydantic import TypeAdapter

from shared.auth import configure_cognito, get_current_user_sub
from shared.db import sync_session
from shared.models import User, Chat
from shared.schemas.user import UserSearchOut
from shared.utils import build_response

# Initialize Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """
    Lambda handler to search users by query string.

    Steps:
    1. Validates JWT token from Authorization header.
    2. Extracts `query` parameter from queryStringParameters.
    3. Finds users matching the query (first_name or last_name), case-insensitive.
    4. Excludes:
       - the current user,
       - users already in a chat with them.

    Args:
        event (dict): API Gateway event.
        context (LambdaContext): Lambda context (unused).

    Returns:
        dict: API Gateway-compatible HTTP response.
    """
    try:
        user_sub = get_current_user_sub(event)
    except Exception as e:
        return build_response(HTTPStatus.UNAUTHORIZED, {"error": str(e)})

    query_params = event.get("queryStringParameters") or {}
    query = query_params.get("query")

    if not query or len(query) < 1:
        return build_response(HTTPStatus.BAD_REQUEST, {"error": "Missing or invalid 'query' parameter"})

    try:
        with sync_session() as db:
            stmt = (
                select(User)
                .where(
                    or_(
                        User.first_name.ilike(f"%{query}%"),
                        User.last_name.ilike(f"%{query}%")
                    ),
                    User.sub != user_sub,
                    ~exists().where(
                        or_(
                            (Chat.user1_sub == user_sub) & (Chat.user2_sub == User.sub),
                            (Chat.user2_sub == user_sub) & (Chat.user1_sub == User.sub)
                        )
                    )
                )
            )
            result = db.execute(stmt)
            users = result.scalars().all()

            json_body = TypeAdapter(list[UserSearchOut]).dump_json(users)
            return {
                "statusCode": HTTPStatus.OK,
                "headers": {"Content-Type": "application/json"},
                "body": json_body
            }

    except Exception as e:
        return build_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
