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
from app.dependencies import (
    get_session,
    JWTBearer,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.Genre], dependencies=[Depends(JWTBearer())])
async def get_genres(
    session: AsyncSession = Depends(get_session),
    name: str = '',
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List genres.
    """
    genres = await crud.genre.get_multi(session=session, name=name, skip=skip, limit=limit)
    return genres


@router.post("/", response_model=schemas.Genre, dependencies=[Depends(JWTBearer())])
async def create_genre(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.GenreCreate,
) -> Any:
    """
    Create new genre.
    """
    genre = await crud.genre.create(session=session, data=data)
    return genre


@router.put("/{id}", response_model=schemas.Genre, dependencies=[Depends(JWTBearer())])
async def update_genre(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
    data: schemas.GenreUpdate,
) -> Any:
    """
    Update a genre.
    """
    genre = await crud.genre.get(session=session, pk=pk)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    genre = await crud.genre.update(session=session, instance=genre, data=data)
    return genre


@router.get("/{id}", response_model=schemas.Genre, dependencies=[Depends(JWTBearer())])
async def get_genre(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Get genre by primary key.
    """
    genre = await crud.genre.get(session=session, pk=pk)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.delete("/{id}", response_model=schemas.Genre, dependencies=[Depends(JWTBearer())])
async def delete_genre(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Delete a genre.
    """
    genre = await crud.genre.get(session=session, pk=pk)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    genre = await crud.genre.remove(session=session, pk=pk)
    return genre
