from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import (
    crud,
    schemas,
)
from app.dependencies.session import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.City])
def get_cities(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List cities.
    """
    cities = crud.city.get_multi(session=session, skip=skip, limit=limit)
    return cities


@router.post("/", response_model=schemas.City)
def create_city(
    *,
    session: AsyncSession = Depends(get_session),
    data: schemas.CityCreate,
) -> Any:
    """
    Create new city.
    """
    city = crud.city.create(session=session, data=data)
    return city


@router.put("/{id}", response_model=schemas.City)
def update_city(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
    data: schemas.CityUpdate,
) -> Any:
    """
    Update a city.
    """
    city = crud.city.get(session=session, pk=pk)
    if not city:
        raise HTTPException(status_code=404, detail="Item not found")
    city = crud.city.update(session=session, instance=city, data=data)
    return city


@router.get("/{id}", response_model=schemas.City)
def get_city(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Get city by primary key.
    """
    city = crud.city.get(session=session, pk=pk)
    if not city:
        raise HTTPException(status_code=404, detail="Item not found")
    return city


@router.delete("/{id}", response_model=schemas.City)
def delete_city(
    *,
    session: AsyncSession = Depends(get_session),
    pk: int,
) -> Any:
    """
    Delete a city.
    """
    city = crud.city.get(session=session, pk=pk)
    if not city:
        raise HTTPException(status_code=404, detail="Item not found")
    city = crud.city.remove(session=session, pk=pk)
    return city
