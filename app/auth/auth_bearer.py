from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_helpers import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, return_token: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.return_token = return_token

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = credentials.credentials
            payload = decode_jwt(token)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            
            if self.return_token:
                return token
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        try:
            payload = decode_jwt(jwtoken)
            return payload 
        except Exception:
            return None
