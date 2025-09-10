from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.book.crud import create_book
from src.api_v1.book.dependencies import get_book_by_id_dependency
from src.api_v1.book.schemas import BookRead, BookCreate
from src.core.models import Book, User
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token

router = APIRouter(prefix="/book", tags=["Books"])


@router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_404_NOT_FOUND)
async def get_book_by_id_view(book: Book = Depends(get_book_by_id_dependency)) -> Book | HTTPException:
    return book


@router.post("/book", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book_view(book_data: BookCreate,
                           user: User = Depends(get_user_by_token),
                           session: AsyncSession = Depends(db_helper.session_getter)) -> Book | HTTPException:
    return await create_book(book_data=book_data,
                             user=user,
                             session=session)