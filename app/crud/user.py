from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

from fastapi.exceptions import HTTPException
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
    async def get_by_email(
            self, session: AsyncSession,
            email: str
    ) -> Optional[User]:
        async with session.begin():
            query = select(User).filter_by(email=email)
            result = await session.execute(query)
            instance = result.fetchone()
        return instance

    async def create(
            self, session: AsyncSession, *, data: UserCreate
    ) -> User:
        async with session.begin():
            data.password = get_password_hash(password=data.password)
            data = dict(data)

            # city primary key existing validation
            city = await session.get(City, data.get('city_id'))
            if not city:
                raise HTTPException(status_code=404, detail='City not found')

            # duplicate user validation
            duplicate = await session.execute(
                select(User).filter_by(email=data.get('email'))
            )
            if duplicate.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail='User with such email already exists'
                )

            # creating user if everything is fine
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
        instance_data = dict(data)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        # city primary key existing validation
        city = await session.get(City, update_data.get('city_id'))
        if not city:
            raise HTTPException(status_code=404, detail='City not found')

        # duplicate user validation
        duplicate = await session.execute(
            select(User).filter_by(email=update_data.get('email'))
        )
        if duplicate.fetchone():
            raise HTTPException(
                status_code=404,
                detail='User with such email already exists'
            )

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
