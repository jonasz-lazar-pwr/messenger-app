# === handlers/health_check_secure.py ===
"""
Secure Health Check Lambda Handler.

This AWS Lambda function performs a simple health check
that requires a valid JWT token in the `Authorization` header.

If the token is valid and contains a `sub`, returns HTTP 200.
Otherwise, returns HTTP 401 Unauthorized.

Triggered by:
    GET /api/health/authenticated

Required environment variables:
    - COGNITO_POOL_ID
    - COGNITO_CLIENT_ID
    - COGNITO_ISSUER_URL
"""

from shared.auth import configure_cognito, get_current_user_sub
from shared.utils import build_response

# Initialize Cognito verifier on cold start
configure_cognito()

def handler(event, context):
    """
    Synchronous Lambda entry point for secure health check.

    Args:
        event (dict): API Gateway event with headers including JWT.
        context (LambdaContext): Lambda runtime metadata (unused).

    Returns:
        dict: API Gateway-compatible HTTP response.
    """
    try:
        user_sub = get_current_user_sub(event)
        return build_response(200, {
            "status": "ok",
            "authenticated_as": user_sub
        })
    except Exception as e:
        return build_response(401, {
            "error": f"Unauthorized: {str(e)}"
        })
