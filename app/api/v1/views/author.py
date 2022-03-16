from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    crud,
    schemas,
)
from app.dependencies.session import get_session

router = APIRouter()


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
