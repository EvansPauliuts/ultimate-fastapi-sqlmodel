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

#
# class ItemInDBBase(ItemBase):
#     id: int
#     title: str
#
#     class Config:
#         orm_mode = True
#
#
# class Item(ItemInDBBase):
#     pass
#
#
# class ItemInDB(ItemInDBBase):
#     pass
