from datetime import datetime

from pytest import fixture, mark
from fastapi.testclient import TestClient
from http import HTTPStatus

from library.db_models import BookModel, BorrowModel
from main import app


@fixture()
def client() -> TestClient:
    return TestClient(app)


@fixture()
def book(db_session) -> BookModel:
    book = BookModel(title="Some title", author="Joe doe", serial_number="000000")
    db_session.add(book)
    db_session.commit()
    return book


@fixture()
def borrow(db_session, book) -> BorrowModel:
    borrow = BorrowModel(
        book_id=book.id, borrower_id="000000", borrowed_at=datetime(2024, 8, 26, 12, 0)
    )
    db_session.add(borrow)
    db_session.commit()
    return borrow


def test_list_books(client, book, borrow):
    response = client.get("/api/books")
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == [
        {
            "author": "Joe doe",
            "id": 1,
            "serial_number": "000000",
            "title": "Some title",
            "borrows": [
                {
                    "id": borrow.id,
                    "borrowed_at": datetime(2024, 8, 26, 12, 0).isoformat(),
                    "borrower_id": "000000",
                    "returned_at": None,
                }
            ],
        }
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


def test_borrow_non_existing_book(client, db_session, book):
    response = client.post(
        f"/api/books/{book.id + 1}/borrow", json={"borrower_id": "000000"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert db_session.query(BookModel).filter(BookModel.id == book.id).count() == 1


@mark.parametrize(
    "data",
    [
        {
            "borrower_id": "abcdef",
        },
        {
            "borrower_id": "000",
        },
        {
            "borrower_id": "000000000",
        },
        {
            "borrower_id": "000 000",
        },
    ],
)
def test_borrow_with_invalid_borrower_number(client, db_session, data, book):
    response = client.post(f"/api/books/{book.id}/borrow")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
    assert db_session.query(BorrowModel).count() == 0


def test_borrow_book(client, db_session, book):
    response = client.post(
        f"/api/books/{book.id}/borrow", json={"borrower_id": "000000"}
    )
    assert response.status_code == HTTPStatus.OK.value
    borrow = db_session.query(BorrowModel).first()
    assert borrow.book_id == book.id
    assert borrow.borrower_id == "000000"


def test_can_not_borrow_already_borrowed_book(client, db_session, book):
    borrow = BorrowModel(book_id=book.id, borrower_id="000000")
    db_session.add(borrow)
    db_session.commit()
    response = client.post(
        f"/api/books/{book.id}/borrow", json={"borrower_id": "000000"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value


def test_can_borrow_borrowed_and_returned_book(client, db_session, book):
    borrow = BorrowModel(
        book_id=book.id, borrower_id="000000", returned_at=datetime.utcnow()
    )
    db_session.add(borrow)
    db_session.commit()
    response = client.post(
        f"/api/books/{book.id}/borrow", json={"borrower_id": "000000"}
    )
    assert response.status_code == HTTPStatus.OK.value


def test_return_book(client, db_session, book):
    borrow = BorrowModel(book_id=book.id, borrower_id="000000")
    db_session.add(borrow)
    db_session.commit()
    response = client.post(
        f"/api/books/{book.id}/return", json={"borrower_id": "000000"}
    )
    db_session.refresh(borrow)
    assert response.status_code == HTTPStatus.OK.value
    assert borrow.returned_at is not None


def test_return_non_existing_book(client, db_session, book):
    borrow = BorrowModel(book_id=book.id, borrower_id="000000")
    db_session.add(borrow)
    db_session.commit()
    response = client.post(
        f"/api/books/{book.id+1}/return", json={"borrower_id": "000000"}
    )
    db_session.refresh(borrow)
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert borrow.returned_at is None


def test_return_non_borrowed_book(client, db_session, book):
    response = client.post(
        f"/api/books/{book.id}/return", json={"borrower_id": "000000"}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
