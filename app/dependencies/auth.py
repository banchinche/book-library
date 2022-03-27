from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=403,
                    detail='Invalid authentication scheme.'
                )
            self.verify_jwt_token(credentials.credentials)
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail='Invalid authorization code.'
            )

    def verify_jwt_token(self, token: str) -> bool:
        print(token)
        payload = decode_token(token=token)
        print(payload)
        if payload:
            return True
        return False
