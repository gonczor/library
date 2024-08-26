from pydantic import BaseModel, field_validator


class BookData(BaseModel):
    id: int
    serial_number: str
    title: str
    author: str

    class Config:
        orm_mode = True


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
