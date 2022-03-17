from typing import (
    Any,
    Dict,
    Union,
)

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.city import City
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorCRUD(
    DataAccessLayerBase[Author, AuthorCreate, AuthorUpdate]
):
    async def create(
            self, session: AsyncSession, *, data: AuthorCreate
    ) -> Author:
        data = dict(data)
        async with session.begin():
            city = await session.get(City, data.get('city_id'))
            if not city:
                raise HTTPException(status_code=404, detail='City not found')
            instance = self.model(**data)  # noqa
            session.add(instance)
        return instance

    async def update(
        self,
        session: AsyncSession,
        *,
        instance: Author,
        data: Union[Author, Dict[str, Any]]
    ) -> Author:
        instance_data = dict(data)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
        city = await session.get(City, update_data.get('city_id'))
        if not city:
            raise HTTPException(status_code=404, detail='City not found')
        for field in instance_data:
            if field in update_data:
                setattr(instance, field, update_data[field])
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    # TODO: probably change remove for author
    #       cause of books relation


author = AuthorCRUD(Author)
