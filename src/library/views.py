from fastapi import APIRouter

from library.models import Book

router = APIRouter(prefix="/api")


@router.get("/books")
async def list_books() -> list[Book]:
    data = [Book(title="Factfullness"), Book(title="Trust")]
    return data
