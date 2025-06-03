# === shared/auth.py ===
"""
JWT authentication and AWS Cognito token validation utilities.

This module provides reusable authentication logic for AWS Lambda handlers
in a serverless architecture using AWS Cognito and JSON Web Tokens (JWT).

It supports:
- Loading Cognito configuration from environment variables.
- Verifying JWT tokens using the Cognito JWKS endpoint.
- Extracting the authenticated user's `sub` from event headers.

Environment Variables:
    COGNITO_POOL_ID (str): Cognito User Pool ID.
    COGNITO_CLIENT_ID (str): Cognito App Client ID.
    COGNITO_ISSUER_URL (str): Issuer base URL (e.g., https://cognito-idp.us-east-1.amazonaws.com).

Usage Example:
    from shared.auth import configure_cognito, get_current_user_sub

    configure_cognito()

    def handler(event, context):
        user_sub = get_current_user_sub(event)
        ...
"""

import os
import requests
from jose import jwt
from jose.exceptions import JWTError

JWKS_CACHE = {}
JWKS_URL = None
CLIENT_ID = None
ISSUER = None


def configure_cognito():
    """
    Load and cache AWS Cognito configuration from environment variables.

    This must be called once per Lambda cold start to initialize:
    - Cognito JWKS URL
    - Client ID
    - Issuer URL

    Raises:
        KeyError: If any required environment variable is missing.
    """
    global JWKS_URL, CLIENT_ID, ISSUER

    client_id = os.environ["COGNITO_CLIENT_ID"]
    issuer_url = os.environ["COGNITO_ISSUER_URL"].rstrip("/")

    CLIENT_ID = client_id
    ISSUER = issuer_url
    JWKS_URL = f"{ISSUER}/.well-known/jwks.json"


def get_current_user_sub(event: dict) -> str:
    """
    Extract and return the Cognito 'sub' (subject ID) from the JWT in the event.

    This function validates the token and returns the authenticated user's ID.

    Args:
        event (dict): Lambda event containing the 'Authorization' header.

    Returns:
        str: The Cognito user's 'sub' claim from the decoded JWT payload.

    Raises:
        Exception: If the token is missing, invalid, or 'sub' is not present.
    """
    payload = get_token_payload(event)
    sub = payload.get("sub")
    if not sub:
        raise Exception("Missing 'sub' in token payload.")
    return sub


def get_token_payload(event: dict) -> dict:
    """
    Extract and verify the JWT token from Lambda event headers.

    Decodes the JWT using the JWKS public key from Cognito and validates claims.

    Args:
        event (dict): Lambda event containing the 'Authorization' header.

    Returns:
        dict: The decoded JWT payload.

    Raises:
        Exception: If the header is missing or malformed, if token validation fails,
                   or if the signing key is not found.
    """
    auth_header = event.get("headers", {}).get("authorization") or event.get("headers", {}).get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header")

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        # Cache JWKS
        if not JWKS_CACHE.get("keys"):
            response = requests.get(JWKS_URL)
            response.raise_for_status()
            JWKS_CACHE.update(response.json())

        jwks = JWKS_CACHE["keys"]
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = next((key for key in jwks if key["kid"] == unverified_header["kid"]), None)

        if not rsa_key:
            raise Exception("Unable to find matching key in JWKS")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=ISSUER,
            options={"verify_at_hash": False}
        )

        return payload

    except JWTError as e:
        raise Exception(f"Token validation failed: {str(e)}")

    except Exception as e:
        raise Exception(f"Error verifying token: {str(e)}")
