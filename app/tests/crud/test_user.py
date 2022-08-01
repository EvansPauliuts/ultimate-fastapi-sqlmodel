from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.tests.utils.utils import random_email
from app.tests.utils.utils import random_lower_string
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session


def test_create_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password)
    user_create = crud.user.create(db=session, obj_in=user)
    assert user_create.email == email
    assert hasattr(user_create, "hashed_password")


def test_auth_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password)
    user_create = crud.user.create(db=session, obj_in=user)
    auth_user = crud.user.authenticate(db=session, email=email, password=password)
    assert auth_user
    assert user_create.email == auth_user.email


def test_no_auth_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    auth_user = crud.user.authenticate(db=session, email=email, password=password)
    assert auth_user is None


def test_check_user_is_active(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password)
    user_create = crud.user.create(db=session, obj_in=user)
    is_active = crud.user.is_active(user_create)
    assert is_active is True


def test_check_user_is_inactive(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password, disabled=True)
    user_create = crud.user.create(db=session, obj_in=user)
    is_active = crud.user.is_active(user_create)
    assert is_active


def test_check_user_is_superuser(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password, is_superuser=True)
    user_create = crud.user.create(db=session, obj_in=user)
    is_superuser = crud.user.is_superuser(user_create)
    assert is_superuser is True


def test_check_user_is_not_superuser(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = UserCreate(email=email, password=password)
    user_create = crud.user.create(db=session, obj_in=user)
    is_not_superuser = crud.user.is_superuser(user_create)
    assert is_not_superuser is False


def test_get_user(session: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user = UserCreate(email=email, password=password, is_superuser=True)
    user_create = crud.user.create(db=session, obj_in=user)
    user_2 = crud.user.get(db=session, item_id=user_create.id)
    assert user_2
    assert user_create.email == user_2.email
    assert jsonable_encoder(user_create) == jsonable_encoder(user_2)


def test_update_user(session: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user = UserCreate(email=email, password=password, is_superuser=True)
    user_create = crud.user.create(db=session, obj_in=user)
    new_password = random_lower_string()
    user_update = UserUpdate(password=new_password, is_superuser=True, email=user.email)
    crud.user.update(db=session, db_obj=user_create, obj_in=user_update)
    user_2 = crud.user.get(db=session, item_id=user_create.id)
    assert user_2
    assert user_create.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
