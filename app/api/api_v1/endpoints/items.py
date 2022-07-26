from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.ItemRead)
def create_item(
    *, db: Session = Depends(deps.get_db), item_in: schemas.ItemCreate
) -> Any:
    item = crud.item.create_with_owner(db=db, obj_in=item_in)
    return item


@router.get("/", response_model=list[schemas.ItemRead])
def read_items(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=schemas.ItemRead)
def read_item(*, db: Session = Depends(deps.get_db), item_id: int) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/{item_id}", response_model=schemas.ItemRead)
def update_item(
    *, db: Session = Depends(deps.get_db), item_id: int, item_in: schemas.ItemUpdate
) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=schemas.ItemRead)
def delete_item(*, db: Session = Depends(deps.get_db), item_id: int) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item = crud.item.remove(db=db, item_id=item_id)
    return item
