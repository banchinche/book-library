from typing import (
    Any,
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    crud,
    schemas,
)
from app.dependencies.session import get_session
from app.core.auth.jwt_auth import encode_token


router = APIRouter()


@router.post('/register', response_model=schemas.Token)
async def register(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.create(session=session, data=data)
    return {'access_token': encode_token(user_id=user.id)}


@router.post('/login', response_model=schemas.Token)
async def login(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.UserLogin
) -> Any:
    """
    Login as given User by credentials
    """
    user = await crud.user.authenticate(
        session=session, email=data.email, password=data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    return {'access_token': encode_token(user_id=user.id)}
