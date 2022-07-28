from typing import Any

from app import crud
from app import models
from app import schemas
from app.api import deps
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlmodel import Session

router = APIRouter()


@router.post("/", response_model=schemas.ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.get("/", response_model=list[schemas.ItemRead], status_code=status.HTTP_200_OK)
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )

    return items


@router.get(
    "/{item_id}", response_model=schemas.ItemRead, status_code=status.HTTP_200_OK
)
def read_item(*, db: Session = Depends(deps.get_db), item_id: int) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    return item


@router.put(
    "/{item_id}", response_model=schemas.ItemRead, status_code=status.HTTP_200_OK
)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )

    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=schemas.ItemRead)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    item = crud.item.get(db=db, item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
        )

    item = crud.item.remove(db=db, item_id=item_id)

    return item
