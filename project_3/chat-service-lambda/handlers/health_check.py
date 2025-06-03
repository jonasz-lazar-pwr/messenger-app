# === handlers/health_check.py ===
"""
Public Health Check Lambda Handler.

This AWS Lambda function performs a basic health check that does not require authentication.
It is typically used by load balancers (e.g. ALB) or monitoring systems to verify that
the service is reachable and responsive.

Triggered by:
    GET /api/health
"""

from shared.utils import build_response


def handler(event, context):
    """
    Synchronous Lambda handler for public health check.

    Args:
        event (dict): API Gateway event (unused).
        context (LambdaContext): Lambda runtime metadata (unused).

    Returns:
        dict: API Gateway-compatible HTTP response.
    """
    return build_response(200, {"status": "ok"})
