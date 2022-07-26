from sqlmodel import Session

from app import crud, models
from app.schemas.item import ItemCreate

from .utils import random_lower_string


def create_random_item(db: Session) -> models.Item:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, id=id)
    return crud.item.create_with_owner(db=db, obj_in=item_in)
