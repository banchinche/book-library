from typing import (
    List,
)

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.book import Book, book_genre
from app.models.genre import Genre
from app.schemas.book import BookCreate, BookUpdate
from app.dependencies.session import get_session


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
        async with session.begin():
            genres = data.genres.copy()
            data = dict(data)
            await self.validate(session=session, data=data)
            data.pop('genres')
            instance = Book(**data)  # noqa
            session.add(instance)
        await session.refresh(instance)
        await session.execute(
            insert(book_genre).values(
                [(instance.id, genre) for genre in genres]
            )
        )
        await session.commit()
        # TODO: fix schema or inserting return value with joined load (research this)
        result = await session.scalars(
                select(Book).options(
                    joinedload(Book.genres)
                ).filter_by(id=instance.id)
            )
        instance = result.unique().one()
        return instance


book = BookCRUD(Book)
