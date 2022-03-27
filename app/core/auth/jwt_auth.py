from datetime import (
    datetime,
    timedelta,
    timezone,
)
from fastapi.exceptions import HTTPException
from jwt import (
    decode,
    encode,
    ExpiredSignatureError,
    InvalidSignatureError,

)

from app.core.config import settings


def encode_token(user_id: int) -> bytes:
    payload = {
        'user_id': user_id,
        'exp':
            datetime.now(tz=timezone.utc) +
            timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES)
    }
    return encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    try:
        decoded = decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return decoded
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail='Token is expired.')
    except InvalidSignatureError:
        raise HTTPException(status_code=403, detail='Token has invalid signature.')
