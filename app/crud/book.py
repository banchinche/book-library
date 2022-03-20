from typing import (
    List,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import joinedload

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.book import Book
from app.models.genre import Genre
from app.schemas.book import BookCreate, BookUpdate


class BookCRUD(
    DataAccessLayerBase[Book, BookCreate, BookUpdate]
):
    fk_relations = {
        'author_id': Author
    }
    m2m_relations = {
        'genres': Genre
    }

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Book]:
        async with session.begin():
            scalars = await session.scalars(
                select(Book).options(
                    joinedload(Book.genres)
                ).offset(skip).limit(limit)
            )
            instances = scalars.unique().all()
        return instances

    # TODO: test this
    async def create(
            self, session: AsyncSession, *, data: BookCreate
    ) -> Book:
        genres = data.genres
        instance = await super(BookCRUD, self).create(session=session, data=data)
        await session.execute(instance.genres.insert().values([
            (instance.id, genre) for genre in genres
        ]))
        return instance


book = BookCRUD(Book)
