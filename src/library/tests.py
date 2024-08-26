from pytest import fixture, mark
from fastapi.testclient import TestClient
from http import HTTPStatus

from library.db_models import BookModel
from main import app


@fixture()
def client() -> TestClient:
    return TestClient(app)


@fixture()
def book(db_session):
    book = BookModel(title="Some title", author="Joe doe", serial_number="000000")
    db_session.add(book)
    db_session.commit()
    return book


def test_list_books(client, book):
    response = client.get("/api/books")
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == [
        {"author": "Joe doe", "id": 1, "serial_number": "000000", "title": "Some title"}
    ]


def test_create_book(client, db_session):
    data = {"author": "Joe doe", "serial_number": "000000", "title": "Some title"}
    response = client.post("/api/books", json=data)

    assert response.status_code == HTTPStatus.OK.value
    saved_book = db_session.query(BookModel).first()
    assert saved_book.title == data["title"]
    assert saved_book.author == data["author"]
    assert saved_book.serial_number == data["serial_number"]


@mark.parametrize(
    "data",
    [
        {},
        {"author": "Joe doe", "serial_number": "000000"},
        {"serial_number": "000000", "title": "Some title"},
        {"author": "Joe doe", "title": "Some title"},
    ],
)
def test_create_book_missing_data(client, db_session, data):
    response = client.post("/api/books", json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
    assert db_session.query(BookModel).count() == 0


@mark.parametrize(
    "data",
    [
        {
            "title": "Title",
            "author": "Author",
            "serial_number": "abcdef",
        },
        {
            "title": "Title",
            "author": "Author",
            "serial_number": "000",
        },
        {
            "title": "Title",
            "author": "Author",
            "serial_number": "000000000",
        },
        {
            "title": "Title",
            "author": "Author",
            "serial_number": "000 000",
        },
    ],
)
def test_create_book_invalid_serial_number(client, db_session, data):
    response = client.post("/api/books", json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
    assert db_session.query(BookModel).count() == 0


def test_delete_book(client, db_session, book):
    response = client.delete(f"/api/books/{book.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT.value
    assert db_session.query(BookModel).filter(BookModel.id == book.id).count() == 0


def test_delete_non_existing_book(client, db_session, book):
    response = client.delete(f"/api/books/{book.id + 1}")

    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert db_session.query(BookModel).filter(BookModel.id == book.id).count() == 1
