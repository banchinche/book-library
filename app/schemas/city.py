from typing import Optional
from pydantic import BaseModel


# Shared properties
class CityBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on city creation
class CityCreate(CityBase):
    name: str


# Properties to receive on city update
class CityUpdate(CityBase):
    ...


# Properties shared by models stored in DB
class CityDatabaseBase(CityBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class City(CityDatabaseBase):
    ...


# Properties stored in DB
class CityDatabase(CityDatabaseBase):
    ...
