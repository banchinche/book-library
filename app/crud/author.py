from typing import (
    Any,
    Optional
)

# from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.person import Person
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorCRUD(
    DataAccessLayerBase[Author, AuthorCreate, AuthorUpdate]
):
    async def get(
            self, session: AsyncSession, pk: Any
    ) -> Optional[Author]:
        async with session.begin():
            query = select(
                Author.id,
                Person.first_name,
                Person.last_name,
                Person.birth_date,
                Person.city_id
            ).join(Author.person).filter_by(id=pk)
            result = await session.execute(query)
            instance = result.fetchone()
        return instance


author = AuthorCRUD(Author)
