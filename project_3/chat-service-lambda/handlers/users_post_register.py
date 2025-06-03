# === handlers/users_post_register.py ===
"""
Register a new user based on JWT token.

This AWS Lambda function decodes a JWT token from the Authorization header
and registers the user in the database if not already present.

Triggered by:
    POST /api/users/register

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

from shared.auth import configure_cognito, get_token_payload
from shared.db import sync_session
from shared.models import User
from shared.schemas.user import UserRegisterOut
from shared.utils import build_response

REQUIRED_FIELDS = ["sub", "email", "given_name", "family_name"]

# Initialize Cognito verifier on cold start
configure_cognito()


def handler(event, context):
    """
    Register a new user using data from a validated JWT.

    Args:
        event (dict): API Gateway event with JWT in headers.
        context (LambdaContext): Lambda runtime context (unused).

    Returns:
        dict: API Gateway-compatible HTTP response.
    """
    try:
        payload = get_token_payload(event)

        missing = [f for f in REQUIRED_FIELDS if f not in payload]
        if missing:
            return build_response(
                HTTPStatus.BAD_REQUEST,
                {"detail": f"Missing required field(s): {', '.join(missing)}"}
            )
    except Exception as e:
        return build_response(
            HTTPStatus.UNAUTHORIZED,
            {"detail": f"Unauthorized: {str(e)}"}
        )

    try:
        with sync_session() as db:
            user = db.execute(select(User).where(User.sub == payload["sub"])).scalar_one_or_none()

            if user:
                return build_response(HTTPStatus.NO_CONTENT)

            db.add(User(
                sub=payload["sub"],
                email=payload["email"],
                first_name=payload["given_name"],
                last_name=payload["family_name"]
            ))
            db.commit()

        return build_response(
            HTTPStatus.CREATED,
            UserRegisterOut(message="User created successfully").model_dump()
        )

    except Exception as e:
        return build_response(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {"error": f"Internal error: {str(e)}"}
        )
