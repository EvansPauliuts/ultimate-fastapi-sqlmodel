from typing import Generator

from sqlmodel import Session

from app.db.session import engine


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
