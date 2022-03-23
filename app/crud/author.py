from typing import (
    Any,
    Dict,
    Union,
)

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.city import City
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorCRUD(
    DataAccessLayerBase[Author, AuthorCreate, AuthorUpdate]
):
    fk_relations = {
        'city_id': City
    }
    m2m_relations = None

    async def create(
            self, session: AsyncSession, *, data: AuthorCreate
    ) -> Author:
        data = dict(data)
        async with session.begin():
            await self.validate(session=session, data=data)
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
        instance_data = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        await self.validate(session=session, data=update_data)

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
