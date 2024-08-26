from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from library.db_models import BookModel, BorrowModel
from library.errors import BookNotFound, BookAlreadyBorrowed, BookNotBorrowed
from library.models import BookCreateData, BookBorrowData


def create_book_service(create_data: BookCreateData, db: Session) -> BookModel:
    db_book = BookModel(**create_data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book_service(book_id: int, db: Session) -> None:
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book is None:
        raise BookNotFound()
    db.query(BookModel).filter(BookModel.id == book_id).delete()
    db.commit()


def borrow_book_service(
    book_id: int, borrow_data: BookBorrowData, db: Session
) -> BookModel:
    book = (
        db.query(BookModel)
        .options(joinedload(BookModel.borrows))
        .filter(BookModel.id == book_id)
        .first()
    )

    if book is None:
        raise BookNotFound()
    if book.borrows and book.borrows[0].returned_at is None:
        raise BookAlreadyBorrowed()
    borrow = BorrowModel(book_id=book_id, borrower_id=borrow_data.borrower_id)
    db.add(borrow)
    db.commit()
    db.refresh(book)
    return book


def return_book_service(book_id: int, db: Session) -> BookModel:
    book = (
        db.query(BookModel)
        .options(joinedload(BookModel.borrows))
        .filter(BookModel.id == book_id)
        .first()
    )

    if book is None:
        raise BookNotFound()
    if not book.borrows:
        raise BookNotBorrowed()
    book.borrows[0].returned_at = datetime.utcnow()
    db.add(book.borrows[0])
    db.commit()
    return book
