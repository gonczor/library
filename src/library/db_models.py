from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(Integer, unique=True)
    title = Column(String)
    author = Column(String)
    is_rented = Column(Boolean)
