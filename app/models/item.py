from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str = Field(index=True)

    owner_id: int | None = Field(default=None, foreign_key="user.id")
    owner: str | None = Relationship(back_populates="items")
