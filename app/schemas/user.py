from pydantic import EmailStr
from sqlmodel import SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
