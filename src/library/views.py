from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from library.db_models import BookModel
from library.models import Book

router = APIRouter(prefix="/api")


@router.get("/books", response_model=list[Book])
def list_books(db: Session = Depends(get_db)):
    data = db.query(BookModel).filter().all()
    return data
