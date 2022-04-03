from typing import (
    List,
    Optional,
)

from datetime import date
from decimal import Decimal
from pydantic import (
    BaseModel,
)


class GenreIdentifier(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# Shared properties
class BookBase(BaseModel):
    title: Optional[str] = None
    release_date: Optional[date] = None
    price: Optional[Decimal] = None
    author_id: Optional[int] = None


# Properties to receive on book creation
class BookCreate(BookBase):
    title: str
    release_date: date
    price: Decimal
    author_id: int
    genres: List[int]


# Properties to receive on book update
class BookUpdate(BookBase):
    title: Optional[str] = None
    release_date: Optional[date] = None
    price: Optional[Decimal] = None
    author_id: Optional[int] = None
    genres: Optional[List[int]] = None


# Properties shared by models stored in DB
class BookDatabaseBase(BookBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Book(BookDatabaseBase):
    genres: List[GenreIdentifier] = list()


# Properties stored in DB
class BookDatabase(BookDatabaseBase):
    ...
