from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy.sql.schema import Column
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel
from sqlmodel import VARCHAR

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    full_name: str = Field(max_length=256, nullable=True)
    email: EmailStr = Field(
        sa_column=Column("email", VARCHAR, unique=True, index=True, nullable=False)
    )
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    items: list["Item"] = Relationship(back_populates="user")
