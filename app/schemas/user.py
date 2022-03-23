from typing import Optional

from datetime import date
from pydantic import (
    BaseModel,
    EmailStr,
)


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    city_id: Optional[int] = None


# Properties to receive on user creation
class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    birth_date: date
    city_id: int


# Properties to receive on user update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserDatabaseBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserDatabaseBase):
    ...


# Properties stored in DB
class UserDatabase(UserDatabaseBase):
    password: str
