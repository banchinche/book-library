from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# TODO: validate queries for every method
class DataAccessLayerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Args:
            model: A SQLAlchemy model class
        """
        self.model = model

    # ok
    async def get(
            self, session: AsyncSession, pk: Any
    ) -> Optional[ModelType]:
        async with session.begin():
            instance = await session.get(self.model, pk)
        return instance

    # ok
    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        async with session.begin():
            query = select(self.model).offset(skip).limit(limit)
            result = await session.execute(query)
        instances = result.scalars().all()
        return instances

    # ok
    async def create(
            self, session: AsyncSession, *, data: CreateSchemaType
    ) -> ModelType:
        data = jsonable_encoder(obj=data)
        async with session.begin():
            instance = self.model(**data)
            session.add(instance)
        return instance

    # TODO: rewrite this
    def update(
        self,
        session: AsyncSession,
        *,
        instance: ModelType,
        data: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        instance_data = jsonable_encoder(instance)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
        for field in instance_data:
            if field in update_data:
                setattr(instance, field, update_data[field])
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    # not working !!!
    # TODO: validate and correct this
    async def remove(self, session: AsyncSession, *, pk: int) -> ModelType:
        async with session.begin():
            instance = await session.get(self.model, pk)
            session.delete(instance)
            session.commit()
        return instance
