from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    full_name: str = Field(index=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True}, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    items: list["Item"] = Relationship(back_populates="user")
