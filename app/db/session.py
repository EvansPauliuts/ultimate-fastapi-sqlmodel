from sqlmodel import SQLModel, create_engine

from app.core.config import settings

sqlite_file_name = settings.SQLMODEL_DATABASE_CLIENT
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def session_db() -> None:
    SQLModel.metadata.create_all(engine)
