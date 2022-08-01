from typing import Any

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.core.config import settings
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlmodel import Session

router = APIRouter()


@router.get("/", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
def read_users(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    *, db: Session = Depends(deps.get_db), user_in: schemas.UserCreate
) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    if password is not None:
        user_in.password = password

    if full_name is not None:
        user_in.full_name = full_name

    if email is not None:
        user_in.email = email

    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    return user


@router.get("/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )

    user = crud.user.get_by_email(db, email=email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )

    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.get("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud.user.get(db, item_id=user_id)

    if user == current_user:
        return user

    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )

    return user


@router.put("/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def update_user(
    *, db: Session = Depends(deps.get_db), user_id: int, user_in: schemas.UserUpdate
) -> Any:
    user = crud.user.get(db, uuid=user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )

    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    return user
