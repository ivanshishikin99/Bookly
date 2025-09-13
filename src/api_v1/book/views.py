from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.author.crud import get_author_by_id
from src.api_v1.author.dependencies import get_author_by_id_dependency
from src.api_v1.book.crud import create_book, update_book_partial, update_book_full, delete_book, get_books_by_author
from src.api_v1.book.dependencies import get_book_by_id_dependency
from src.api_v1.book.schemas import BookRead, BookCreate, BookUpdatePartial, BookUpdateFull
from src.core.models import Book, User, Author
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token

router = APIRouter(prefix="/book", tags=["Books"])


@cache(expire=60)
@router.get("/{book_id}", response_model=BookRead, status_code=status.HTTP_404_NOT_FOUND)
async def get_book_by_id_view(book: Book = Depends(get_book_by_id_dependency)) -> BookRead | HTTPException:
    return book


@router.post("/book", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book_view(book_data: BookCreate,
                           user: User = Depends(get_user_by_token),
                           session: AsyncSession = Depends(db_helper.session_getter)) -> Book | HTTPException:
    return await create_book(book_data=book_data,
                             user=user,
                             session=session)


@router.patch("/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def update_book_partial_view(book_data: BookUpdatePartial,
                                   user: User = Depends(get_user_by_token),
                                   book: Book = Depends(get_book_by_id_dependency),
                                   session: AsyncSession = Depends(db_helper.session_getter)) -> Book | HTTPException:
    return await update_book_partial(book_data=book_data,
                                     user=user,
                                     book=book,
                                     session=session)


@router.put("/{book_id}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def update_book_full_view(book_data: BookUpdateFull,
                                user: User = Depends(get_user_by_token),
                                book: Book = Depends(get_book_by_id_dependency),
                                session: AsyncSession = Depends(db_helper.session_getter)) -> Book | HTTPException:
    return await update_book_full(book_data=book_data,
                                  user=user,
                                  book=book,
                                  session=session)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_view(user: User = Depends(get_user_by_token),
                           book: Book = Depends(get_book_by_id_dependency),
                           session: AsyncSession = Depends(db_helper.session_getter)):
    return await delete_book(user=user,
                             book=book,
                             session=session)


@cache(expire=60)
@router.get("/{author_id}/books", status_code=status.HTTP_200_OK, response_model=list[BookRead])
async def get_books_by_author_view(author: Author = Depends(get_author_by_id_dependency),
                                   session: AsyncSession = Depends(db_helper.session_getter)) -> list[BookRead]:
    return await get_books_by_author(author=author,
                                     session=session)