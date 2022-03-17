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


@router.get("/", response_model=List[schemas.Author])
async def get_authors(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List authors.
    """
    authors = await crud.author.get_multi(session=session, skip=skip, limit=limit)
    return authors


@router.post("/", response_model=schemas.Author)
async def create_author(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.AuthorCreate,
) -> Any:
    """
    Create new author.
    """
    author = await crud.author.create(session=session, data=data)
    return author


@router.put("/{id}", response_model=schemas.Author)
async def update_author(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
    data: schemas.AuthorUpdate,
) -> Any:
    """
    Update an author.
    """
    author = await crud.author.get(session=session, pk=pk)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author = await crud.author.update(session=session, instance=author, data=data)
    return author


@router.get("/{id}", response_model=schemas.Author)
async def get_author(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Get author by primary key.
    """
    author = await crud.author.get(session=session, pk=pk)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{id}", response_model=schemas.Author)
async def delete_author(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Delete an author.
    """
    author = await crud.author.get(session=session, pk=pk)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author = await crud.author.remove(session=session, pk=pk)
    return author
