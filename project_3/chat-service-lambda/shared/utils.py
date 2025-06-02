# === shared/utils.py ===
"""
Utility functions for Lambda handlers.

This module provides reusable utility functions to support AWS Lambda-based
microservices.

Functions:
    - build_response: Wraps the payload in a standard API Gateway-compatible response.
    - parse_body: Parses the JSON body from an API Gateway event.
"""

import json
from typing import Any


def build_response(status_code: int, body: Any = None) -> dict:
    """
    Builds a standard HTTP JSON response for API Gateway integration.

    Adds default CORS headers allowing all origins and headers (dev mode).

    Args:
        status_code (int): HTTP status code.
        body (dict | None): Response payload or None (for 204).

    Returns:
        dict: API Gateway-compatible response.
    """
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH"
    }

    if status_code == 204:
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": ""
        }

    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body or {})
    }

def parse_body(event: dict) -> dict:
    """
    Parses and returns the JSON body from an API Gateway event.

    Args:
        event (dict): The Lambda event containing 'body' as a JSON string.

    Returns:
        dict: Parsed JSON body.

    Raises:
        ValueError: If body is missing or cannot be parsed as JSON.
    """
    try:
        return json.loads(event.get("body", "") or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in request body")

