from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session
from typing import Generator

from app import models, schemas
from app.core.config import settings
from app.db.session import engine


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
