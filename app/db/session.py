from app.core.config import settings
from sqlmodel import create_engine
from sqlmodel import SQLModel

sqlite_file_name = settings.SQLMODEL_DATABASE_CLIENT
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
