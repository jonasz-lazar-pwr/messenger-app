# api/routes/proxy.py

import httpx
from fastapi import APIRouter, Request, HTTPException, Response
from api.core.config import settings

router = APIRouter()


@router.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    summary="Proxy endpoint",
    description="Proxies the request to the appropriate microservice based on the path.",
    # dependencies=[Depends(JWTBearer())]
)
async def proxy(full_path: str, request: Request):
    """
    Forwards incoming requests to the corresponding microservice.
    - Matches path prefixes to determine the destination service.
    - Supports all HTTP methods (GET, POST, PUT, DELETE, PATCH).
    """
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

    # Body: stream it to handle JSON/multipart/form etc.
    body = await request.body()

    # 4. Forward the request
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

    # 5. Return the response 1:1
    return Response(
        content=proxy_response.content,
        status_code=proxy_response.status_code,
        headers=dict(proxy_response.headers),
        media_type=proxy_response.headers.get("content-type")
    )