from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.api.deps import get_db
from app.db.init_db import init_db
from app.main import app
from app.tests.utils.utils import get_superuser_token_headers

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


@pytest.fixture(name="session")
def session_fixture() -> Generator:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator:
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)
