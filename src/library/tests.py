from pytest import fixture
from fastapi.testclient import TestClient

from database import get_db
from library.db_models import BookModel
from main import app


@fixture()
def client() -> TestClient:
    return TestClient(app)


@fixture()
def book(db_session):
    book = BookModel(title="Some title")
    db_session.add(book)
    db_session.commit()


def test_list_books(client, book):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Some title"}]
