from typing import Optional
from pydantic import BaseModel


# Shared properties
class GenreBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on genre creation
class GenreCreate(GenreBase):
    name: str


# Properties to receive on genre update
class GenreUpdate(GenreBase):
    ...


# Properties shared by models stored in DB
class GenreDatabaseBase(GenreBase):
    id: int
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Genre(GenreDatabaseBase):
    ...


# Properties stored in DB
class GenreDatabase(GenreDatabaseBase):
    ...
