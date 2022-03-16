from typing import Optional

from datetime import date
from pydantic import BaseModel


# Shared properties
class AuthorBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    city_id: Optional[int] = None


# Properties to receive on city creation
class AuthorCreate(AuthorBase):
    first_name: str
    last_name: str
    birth_date: date
    city_id: int


# Properties to receive on city update
class AuthorUpdate(AuthorBase):
    ...


# Properties shared by models stored in DB
class AuthorDatabaseBase(AuthorBase):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    city_id: int

    # class Config:
    #     orm_mode = True


# Properties to return to client
class Author(AuthorDatabaseBase):
    ...


# Properties stored in DB
class AuthorDatabase(AuthorDatabaseBase):
    ...
