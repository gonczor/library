from pytest import fixture
from fastapi.testclient import TestClient

from main import app


@fixture()
def client() -> TestClient:
    return TestClient(app)


def test_list_books(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert response.json() == [{"title": "Factfullness"}, {"title": "Trust"}]
