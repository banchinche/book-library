from typing import (
    Any,
    Optional,
    Union,
)

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.core.security import get_password_hash
from app.crud.base import DataAccessLayerBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD(
    DataAccessLayerBase[User, UserCreate, UserUpdate]
):
    # TODO: test this
    async def get_by_email(
            self, session: AsyncSession,
            email: str
    ) -> Optional[User]:
        async with session.begin():
            query = select(self.model).filter_by(email=email)
            result = await session.execute(query)
            instance = result.fetchone()
        return instance

    # TODO: test this
    async def create(
            self, session: AsyncSession, *, data: UserCreate
    ) -> User:
        async with session.begin():
            print('BEFORE hashing', data.password)
            data.password = get_password_hash(password=data.password)
            print('AFTER hashing', data.password)
            data = dict(data)
            print('DATA', data)
            instance = self.model(**data)  # noqa
            session.add(instance)
        return instance
