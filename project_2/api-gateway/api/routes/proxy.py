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
    # 1. Determine microservice based on the path
    if full_path.startswith(("messages", "chats", "users")):
        service_host = settings.CHAT_SERVICE_HOST
        service_port = settings.CHAT_SERVICE_PORT
    elif full_path.startswith("media"):
        service_host = settings.MEDIA_SERVICE_HOST
        service_port = settings.MEDIA_SERVICE_PORT
    elif full_path.startswith("notifications"):
        service_host = settings.NOTIFICATION_SERVICE_HOST
        service_port = settings.NOTIFICATION_SERVICE_PORT
    else:
        raise HTTPException(status_code=404, detail="Service not found for this path.")

    # 2. Prepare the forwarded URL
    target_url = f"http://{service_host}:{service_port}/{full_path}"

    # 3. Extract method, headers, params, body
    method = request.method
    headers = dict(request.headers)
    query_params = request.query_params

    # Inject token payload as custom header
    token = credentials.credentials
    token_payload = jwt_bearer.get_verified_payload(token)
    headers["X-User-Payload"] = json.dumps(token_payload)

    # Optional: decide whether to keep forwarding the Authorization header
    # headers["Authorization"] = f"Bearer {credentials.credentials}"

    # 4. Body: stream it to handle JSON/multipart/form etc.
    body = await request.body()

    # 5. Forward the request
    async with httpx.AsyncClient() as client:
        try:
            proxy_response = await client.request(
                method=method,
                url=target_url,
                content=body,
                params=query_params,
                headers=headers,
                timeout=30.0
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting service: {str(e)}")

    # 6. Return the response 1:1, but avoid double compression issues
    return Response(
        content=proxy_response.content,
        status_code=proxy_response.status_code,
        headers={key: value for key, value in proxy_response.headers.items() if key.lower() != "content-encoding"},
        media_type=proxy_response.headers.get("content-type")
    )
