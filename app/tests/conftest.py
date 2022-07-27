from typing import Generator

import pytest
from app.api.deps import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture() -> Generator:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator:
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
