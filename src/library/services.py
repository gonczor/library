from sqlalchemy.orm import Session

from library.db_models import BookModel
from library.errors import BookNotFound
from library.models import BookCreateData


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


def borrow_book_service():
    pass


def return_book_service():
    pass
