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

from app.core.security import (
    get_password_hash,
    verify_password,
)
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

    async def authenticate(
            self,
            session: AsyncSession,
            email: str,
            password: str
    ) -> Optional[User]:
        instance = await self.get_by_email(session=session, email=email)
        if not instance:
            return None
        if not verify_password(password, instance.password):
            return None
        return instance

    async def get_by_email(
            self, session: AsyncSession,
            email: str,
    ) -> Optional[User]:
        query = select(User).filter_by(email=email)
        result = await session.scalars(query)
        instance = result.first()
        return instance

    async def get_multi(
        self, session: AsyncSession, *,
        email: str = '', skip: int = 0, limit: int = 100
    ) -> User:
        if email:
            query = select(User).filter(User.email.ilike(f'%{email}%'))  # noqa
        else:
            query = select(User)
        query = query.offset(skip).limit(limit)
        async with session.begin():
            result = await session.execute(query)
        instances = result.scalars().unique().all()
        return instances

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
