from sqlalchemy import Column, Integer, String

from database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True)
    title = Column(String)
    author = Column(String)


class BorrowModel(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(String)
