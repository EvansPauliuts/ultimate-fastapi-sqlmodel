from typing import Any

from app.core.security import get_password_hash
from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from sqlmodel import select
from sqlmodel import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        get_email_user = select(User).where(User.email == email)
        return db.exec(get_email_user).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        valid_user = self.get_by_email(db, email=email)

        if not valid_user:
            return None

        if not verify_password(password, valid_user.hashed_password):
            return None

        return valid_user

    def is_active(self, user_in: User) -> bool:
        return user_in.is_active

    def is_superuser(self, user_in: User) -> bool:
        return user_in.is_superuser


user = CRUDUser(User)
