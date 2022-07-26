from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, item_id: int) -> ModelType | None:
        item = db.get(self.model, item_id)
        return item

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        get_items = select(self.model)
        return db.exec(get_items.offset(skip).limit(limit)).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model.from_orm(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        item_data = obj_in.dict(exclude_unset=True)

        for key, value in item_data.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, item_id: int) -> ModelType:
        obj = db.get(self.model, item_id)
        db.delete(obj)
        db.commit()
        return obj
