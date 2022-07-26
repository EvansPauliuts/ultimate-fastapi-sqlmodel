from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from .base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> list[Item]:
    #     return (
    #         db.query(self.model)
    #         .filter(Item.owner_id == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


item = CRUDItem(Item)
