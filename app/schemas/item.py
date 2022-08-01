from sqlmodel import SQLModel


class ItemBase(SQLModel):
    title: str
    description: str


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int


class ItemUpdate(ItemBase):
    pass
