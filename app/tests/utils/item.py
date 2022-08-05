from sqlmodel import Session

from app import crud, models
from app.schemas.item import ItemCreate

from .user import create_random_user
from .utils import random_lower_string


def create_random_item(db: Session, owner_id: int | None = None) -> models.Item:
    if owner_id is None:
        user = create_random_user(db=db)
        owner_id = user.id

    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)

    return crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=owner_id)
