from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
from api.core.config import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.jwks_url = f"{settings.COGNITO_ISSUER_URL.rstrip('/')}/{settings.COGNITO_POOL_ID}/.well-known/jwks.json"
        self.issuer = f"{settings.COGNITO_ISSUER_URL.rstrip('/')}/{settings.COGNITO_POOL_ID}"

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials and credentials.scheme == "Bearer":
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return payload

        raise HTTPException(status_code=403, detail="Invalid authorization credentials.")

    def verify_jwt(self, token: str):
        try:
            jwks = requests.get(self.jwks_url).json()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = next(
                (
                    {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    for key in jwks["keys"]
                    if key["kid"] == unverified_header["kid"]
                ),
                None
            )

            if not rsa_key:
                return None

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.COGNITO_CLIENT_ID,
                issuer=self.issuer,
                options={"verify_at_hash": False}
            )

            return payload

        except Exception:
            return None
