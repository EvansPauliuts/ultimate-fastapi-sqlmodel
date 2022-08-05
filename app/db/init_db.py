import logging

from sqlmodel import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

        if not user:
            user_in = schemas.UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                'Skipping creating superuser. User with email.',
                f'{settings.FIRST_SUPERUSER} already exists.',
            )

    else:
        logger.warning(
            'Skipping creating superuser. FIRST_SUPERUSER needs to be.', 'Error'
        )
