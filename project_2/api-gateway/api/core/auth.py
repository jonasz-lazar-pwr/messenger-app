# api/core/auth.py

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from cachetools import TTLCache
import requests


class CognitoJWTBearer(HTTPBearer):
    _jwks_cache = TTLCache(maxsize=1, ttl=3600)

    def __init__(self, pool_id: str, client_id: str, issuer_url: str, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.pool_id = pool_id
        self.client_id = client_id
        self.issuer = f"{issuer_url.rstrip('/')}/{pool_id}"
        self.jwks_url = f"{self.issuer}/.well-known/jwks.json"

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authorization credentials.")

        token = credentials.credentials
        payload = self.verify_jwt(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return credentials

    def verify_jwt(self, token: str):
        try:
            if 'jwks' not in self._jwks_cache:
                self._jwks_cache['jwks'] = requests.get(self.jwks_url).json()

            jwks = self._jwks_cache['jwks']
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = next(
                (key for key in jwks["keys"] if key["kid"] == unverified_header["kid"]),
                None
            )

            if rsa_key is None:
                return None

            return jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.issuer,
                options={"verify_at_hash": False}
            )
        except Exception:
            return None

    def get_verified_payload(self, token: str) -> dict:
        """
        Shortcut method to get verified payload or raise HTTPException if invalid.
        """
        payload = self.verify_jwt(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return payload
