from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True)
    title = Column(String)
    author = Column(String)

    borrows = relationship(
        "BorrowModel", back_populates="book", order_by="BorrowModel.borrowed_at.desc()"
    )


class BorrowModel(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("BookModel", back_populates="borrows")
