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

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DataAccessLayerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    fk_relations: Optional[Dict[str, Base]] = None
    m2m_relations: Optional[Dict[str, Base]] = None

    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Args:
            model: A SQLAlchemy model class
        """
        self.model = model

    async def get(
            self, session: AsyncSession, pk: Any
    ) -> Optional[ModelType]:
        async with session.begin():
            instance = await session.get(self.model, pk)
        return instance

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        async with session.begin():
            query = select(self.model).offset(skip).limit(limit)
            result = await session.execute(query)
        instances = result.scalars().unique().all()
        return instances

    async def create(
            self, session: AsyncSession, *, data: CreateSchemaType
    ) -> ModelType:
        data = dict(data)
        async with session.begin():
            instance = self.model(**data)
            session.add(instance)
        return instance

    async def update(
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
        await session.commit()
        await session.refresh(instance)
        return instance

    async def remove(self, session: AsyncSession, *, pk: int) -> ModelType:
        async with session.begin():
            instance = await session.get(self.model, pk)
            await session.delete(instance)
        return instance

    async def check_keys_existence(
            self, session: AsyncSession, data: Dict
    ) -> None:
        """
        Validates on primary keys existence that were passed for create/update
        Args:
            session: AsyncSession instance, dependency for getting instances
            data: Dictionary with values that come from view
        """

        if not (self.fk_relations or self.m2m_relations):
            model = self.model.__tablename__.capitalize()
            raise NotImplementedError(f'{model} has no serialized relations')

        errors = dict()
        if self.fk_relations:
            fk_fields = {
                key: value
                for key, value in data.items()
                if key in self.fk_relations and value
            }
            if fk_fields:
                fk_errors = dict()
                for key, identity in fk_fields.items():
                    exists = await session.get(self.fk_relations[key], identity)
                    if not exists:
                        model_name = self.fk_relations[key].__tablename__.capitalize()
                        fk_errors[f'{model_name} error'] = \
                            f'{model_name} with ID {identity} does not exist'
                if fk_errors:
                    errors['foreign_key_errors'] = fk_errors
        if self.m2m_relations:
            m2m_fields = {
                key: value
                for key, value in data.items()
                if key in self.m2m_relations and value
            }
            if m2m_fields:
                m2m_errors = dict()
                for key, identities in m2m_fields.items():
                    for pk in identities:
                        exists = await session.get(self.m2m_relations[key], pk)
                        if not exists:
                            model_name = self.m2m_relations[key].__tablename__.capitalize()
                            m2m_errors[f'{model_name} error'] = \
                                f'{model_name} with ID {pk} does not exist'
                if m2m_errors:
                    errors['many_to_many_errors'] = m2m_errors
        if errors:
            raise HTTPException(status_code=404, detail=errors)

    async def validate(self, session: AsyncSession, data: Dict) -> None:
        await self.check_keys_existence(session=session, data=data)
