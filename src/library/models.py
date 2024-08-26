from datetime import datetime

from pydantic import BaseModel, field_validator


class BorrowData(BaseModel):
    id: int
    borrower_id: str
    borrowed_at: datetime
    returned_at: datetime | None


class BookData(BaseModel):
    id: int
    serial_number: str
    title: str
    author: str
    borrows: list[BorrowData]


class BookCreateData(BaseModel):
    serial_number: str
    title: str
    author: str

    @field_validator("serial_number")
    @classmethod
    def serial_number_must_be_6_digit(cls, v: str) -> str:
        if len(v) != 6:
            raise ValueError("serial number must be a 6-digit number")
        try:
            int(v)
        except ValueError:
            raise ValueError("serial number must be a 6-digit number")
        return v

    class Config:
        orm_mode = True


class BookBorrowData(BaseModel):
    borrower_id: str

    @field_validator("borrower_id")
    @classmethod
    def borrower_id_must_be_6_digit(cls, v: str) -> str:
        if len(v) != 6:
            raise ValueError("borrower_id must be a 6-digit number")
        try:
            int(v)
        except ValueError:
            raise ValueError("borrower_id must be a 6-digit number")
        return v
