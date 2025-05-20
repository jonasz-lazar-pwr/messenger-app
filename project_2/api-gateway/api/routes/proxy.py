# api/routes/proxy.py

import httpx
import json
from fastapi import APIRouter, Request, HTTPException, Response, Depends
from fastapi.security import HTTPAuthorizationCredentials
from api.core.auth import CognitoJWTBearer
from api.core.config import settings

jwt_bearer = CognitoJWTBearer(
    pool_id=settings.COGNITO_POOL_ID,
    client_id=settings.COGNITO_CLIENT_ID,
    issuer_url=settings.COGNITO_ISSUER_URL,
)

router = APIRouter()

@router.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    summary="Proxy endpoint",
    description="Proxies the request to the appropriate microservice based on the path."
)
async def proxy(
    full_path: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(jwt_bearer)
):
    # 1. Extract request data
    method = request.method
    headers = dict(request.headers)
    query_params = request.query_params
    body = await request.body()

    # 2. Set target microservice based on the path
    if full_path.startswith(("messages", "chats", "users")):
        service_host = settings.CHAT_SERVICE_HOST
        service_port = settings.CHAT_SERVICE_PORT
    else:
        raise HTTPException(status_code=404, detail="Unknown path prefix, no matching service.")

    # 3. Build target URL
    target_url = f"http://{service_host}:{service_port}/{full_path}"

    # 4. Inject token payload as custom header
    token = credentials.credentials
    try:
        token_payload = jwt_bearer.get_verified_payload(token)
        headers["X-User-Payload"] = json.dumps(token_payload)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid or expired token.")

    # 5. Forward request to internal service
    try:
        async with httpx.AsyncClient() as client:
            if headers.get("content-type", "").startswith("application/json"):
                parsed_body = json.loads(body or "{}")
                proxy_response = await client.request(
                    method=method,
                    url=target_url,
                    json=parsed_body,
                    params=query_params,
                    headers=headers,
                    timeout=30.0,
                    follow_redirects=True
                )
            else:
                proxy_response = await client.request(
                    method=method,
                    url=target_url,
                    content=body,
                    params=query_params,
                    headers=headers,
                    timeout=30.0,
                    follow_redirects=True
                )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error contacting service: {str(e)}")

    # 6. Return response
    return Response(
        content=proxy_response.content,
        status_code=proxy_response.status_code,
        headers={k: v for k, v in proxy_response.headers.items() if k.lower() != "content-encoding"},
        media_type=proxy_response.headers.get("content-type")
    )
