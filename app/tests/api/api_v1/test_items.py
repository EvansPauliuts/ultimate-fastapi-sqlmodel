from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item


def test_create_item(session: Session, client: TestClient) -> None:
    data = {"title": "Foo", "description": "Fighters"}

    response = client.post(
        f"{settings.API_V1_STR}/items/",
        json=data,
    )
    content = response.json()

    assert response.status_code == 200
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_item(session: Session, client: TestClient) -> None:
    item = create_random_item(session)
    response = client.get(f"{settings.API_V1_STR}/items/{item.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
