from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.book.crud import get_book_by_id
from src.core.models import Book
from src.utils import db_helper


async def get_book_by_id_dependency(book_id: int,
                                    session: AsyncSession = Depends(db_helper)) -> Book | HTTPException:
    try:
        book = await get_book_by_id(book_id=book_id,
                                    session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book