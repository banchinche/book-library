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


@router.get("/", response_model=List[schemas.Book])
async def get_books(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List books.
    """
    books = await crud.book.get_multi(session=session, skip=skip, limit=limit)
    return books


@router.post("/", response_model=schemas.Book)
async def create_book(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.BookCreate,
) -> Any:
    """
    Create new book.
    """

    book = await crud.book.create(session=session, data=data)
    return book


# @router.put("/{id}", response_model=schemas.User)
# async def update_user(
#     *,
#     session: AsyncSession = Depends(get_session),
#     pk: int,
#     data: schemas.UserUpdate,
# ) -> Any:
#     """
#     Update an user.
#     """
#     user = await crud.user.get(session=session, pk=pk)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user = await crud.user.update(session=session, instance=user, data=data)
#     return user


@router.get("/{id}", response_model=schemas.Book)
async def get_book(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Get book by primary key.
    """
    book = await crud.book.get(session=session, pk=pk)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{id}", response_model=schemas.Book)
async def delete_book(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Delete a book.
    """
    book = await crud.book.get(session=session, pk=pk)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book = await crud.book.remove(session=session, pk=pk)
    return book
