from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from library.db_models import BookModel
from library.errors import BookNotFound
from library.models import BookData, BookCreateData
from library.services import create_book_service, delete_book_service

router = APIRouter(prefix="/api")


@router.get("/books", response_model=list[BookData])
def list_books(db: Session = Depends(get_db)):
    data = db.query(BookModel).filter().all()
    return data


@router.post("/books", response_model=BookData)
def create_book(book: BookCreateData, db: Session = Depends(get_db)):
    book = create_book_service(create_data=book, db=db)
    return book


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        delete_book_service(book_id, db)
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    except BookNotFound:
        return Response(status_code=HTTPStatus.NOT_FOUND.value)
