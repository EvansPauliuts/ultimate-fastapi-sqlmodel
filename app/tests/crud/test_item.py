from sqlmodel import Session

from app import crud
from app.schemas.item import ItemCreate, ItemUpdate
from app.tests.utils.utils import random_lower_string


def test_create_item(session: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = crud.item.create_with_owner(db=session, obj_in=item_in)
    assert item.title == title
    assert item.description == description


def test_get_item(session: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = crud.item.create_with_owner(db=session, obj_in=item_in)
    stored_item = crud.item.get(db=session, item_id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description


def test_update_item(session: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = crud.item.create_with_owner(db=session, obj_in=item_in)
    title2 = random_lower_string()
    description2 = random_lower_string()
    item_update = ItemUpdate(title=title2, description=description2)
    item2 = crud.item.update(db=session, db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2


def test_delete_item(session: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = crud.item.create_with_owner(db=session, obj_in=item_in)
    item2 = crud.item.remove(db=session, item_id=item.id)
    item3 = crud.item.get(db=session, item_id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.title == title
    assert item2.description == description
