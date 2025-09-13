from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.book.crud import get_book_by_id
from src.api_v1.book.schemas import BookRead
from src.core.models import Book
from src.utils import db_helper


async def get_book_schema_by_id_dependency(book_id: int,
                                    session: AsyncSession = Depends(db_helper.session_getter)) -> BookRead | HTTPException:
    try:
        book = await get_book_by_id(book_id=book_id,
                                    session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return BookRead(title=book.title,
                    year_of_release=book.year_of_release,
                    author=book.author.full_name,
                    description=book.description)


async def get_book_by_id_dependency(book_id: int,
                                    session: AsyncSession = Depends(db_helper.session_getter)) -> BookRead | HTTPException:
    try:
        book = await get_book_by_id(book_id=book_id,
                                    session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book