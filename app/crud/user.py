from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.core.security import get_password_hash
from app.crud.base import DataAccessLayerBase
from app.models.city import City
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserCRUD(
    DataAccessLayerBase[User, UserCreate, UserUpdate]
):
    fk_relations = {
        'city_id': City
    }
    m2m_relations = None

    async def get_by_email(
            self, session: AsyncSession,
            email: str,
    ) -> Optional[User]:
        query = select(User).filter_by(email=email)
        result = await session.execute(query)
        instance = result.fetchone()
        return instance

    async def validate(
            self,
            session: AsyncSession,
            data: Dict,
    ) -> None:
        await super(UserCRUD, self).validate(session=session, data=data)

        # duplicate user validation
        duplicate = await self.get_by_email(session=session, email=data.get('email'))
        if duplicate:
            raise HTTPException(
                status_code=404,
                detail='User with such email already exists'
            )

    async def create(
            self, session: AsyncSession, *, data: UserCreate
    ) -> User:
        async with session.begin():
            data.password = get_password_hash(password=data.password)
            data = dict(data)

            await self.validate(session=session, data=data)

            instance = User(**data)  # noqa
            session.add(instance)
        return instance

    async def update(
        self,
        session: AsyncSession,
        *,
        instance: User,
        data: Union[User, Dict[str, Any]]
    ) -> User:
        instance_data = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        await self.validate(session=session, data=update_data)

        # updating user information
        if update_data.get('password'):
            update_data['password'] = get_password_hash(
                password=update_data['password']
            )
        for field in instance_data:
            if field in update_data:
                setattr(instance, field, update_data[field])
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


user = UserCRUD(User)
