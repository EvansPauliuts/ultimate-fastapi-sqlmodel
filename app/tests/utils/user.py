from app import crud
from app.models.user import User
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email
from app.tests.utils.utils import random_lower_string
from sqlmodel import Session


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user
