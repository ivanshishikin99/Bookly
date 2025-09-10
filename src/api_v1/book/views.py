from fastapi import APIRouter, status, Depends, HTTPException

from src.api_v1.book.dependencies import get_book_by_id_dependency
from src.api_v1.book.schemas import BookRead
from src.core.models import Book

router = APIRouter(prefix="/book", tags=["Books"])


@router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_404_NOT_FOUND)
async def get_book_by_id_view(book: Book = Depends(get_book_by_id_dependency)) -> Book | HTTPException:
    return book
