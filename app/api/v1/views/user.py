from typing import (
    Any,
    List,
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    crud,
    schemas,
)
from app.dependencies.session import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def get_users(
    session: AsyncSession = Depends(get_session),
    email: str = '',
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List users.
    """
    users = await crud.user.get_multi(
        session=session, email=email, skip=skip, limit=limit
    )
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.create(session=session, data=data)
    return user


@router.put("/{id}", response_model=schemas.User)
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
    data: schemas.UserUpdate,
) -> Any:
    """
    Update an user.
    """
    user = await crud.user.get(session=session, pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.user.update(session=session, instance=user, data=data)
    return user


@router.get("/{id}", response_model=schemas.User)
async def get_user(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Get user by primary key.
    """
    user = await crud.user.get(session=session, pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{id}", response_model=schemas.User)
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Delete an user.
    """
    user = await crud.user.get(session=session, pk=pk)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.user.remove(session=session, pk=pk)
    return user
