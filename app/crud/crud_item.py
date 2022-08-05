from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

from .base import CRUDBase


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


item = CRUDItem(Item)
