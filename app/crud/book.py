from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from fastapi.encoders import jsonable_encoder
from sqlalchemy import (
    delete,
    insert,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import DataAccessLayerBase
from app.models.author import Author
from app.models.book import Book, book_genre
from app.models.genre import Genre
from app.schemas.book import BookCreate, BookUpdate


class BookCRUD(
    DataAccessLayerBase[Book, BookCreate, BookUpdate]
):
    # TODO: as improvement research and change to lazy='joined' in Book model
    #  for uploading model with all relations (genres)
    fk_relations = {
        'author_id': Author
    }
    m2m_relations = {
        'genres': Genre
    }

    async def get(
            self, session: AsyncSession, pk: int
    ) -> Optional[Book]:
        async with session.begin():
            result = await session.scalars(
                select(Book).options(
                    joinedload(Book.genres)
                ).filter_by(id=pk)
            )
            instance = result.unique().first()
        return instance

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
        # TODO: after improvement remove this
        async with session.begin():
            await session.refresh(instance)
            result = await session.scalars(
                        select(Book).options(
                            joinedload(Book.genres)
                        ).filter_by(id=instance.id)
                    )
            instance = result.unique().first()
        return instance

    async def remove(
            self, session: AsyncSession, *, pk: int
    ) -> Book:
        instance = await self.get(session=session, pk=pk)
        async with session.begin():
            await session.delete(instance)
        return instance

    async def update(
        self,
        session: AsyncSession,
        *,
        instance: Book,
        data: Union[BookUpdate, Dict[str, Any]]
    ) -> Book:
        instance_data = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        await self.validate(session=session, data=update_data)
        genres = update_data.pop('genres')
        for field in instance_data:
            if field in update_data:
                setattr(instance, field, update_data[field])
        await session.commit()
        await session.refresh(instance)
        if genres != instance.genres:
            await session.execute(
                delete(book_genre).where(
                    book_genre.c.book_id == instance.id, book_genre.c.genre_id not in genres
                )
            )
            await session.commit()
            await session.execute(
                insert(book_genre).values(
                    [(instance.id, genre) for genre in genres if genre not in instance.genres]
                )
            )
            await session.commit()
        async with session.begin():
            await session.refresh(instance)
            result = await session.scalars(
                        select(Book).options(
                            joinedload(Book.genres)
                        ).filter_by(id=instance.id)
                    )
            instance = result.unique().first()
        return instance


book = BookCRUD(Book)
