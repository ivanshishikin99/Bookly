from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.book.schemas import BookCreate
from src.core.models import Book, User


async def get_book_by_id(book_id: int,
                         session: AsyncSession) -> Book | None:
    book = await session.get(Book, book_id)
    return book


async def create_book(book_data: BookCreate,
                      user: User,
                      session: AsyncSession) -> Book | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super user are allowed to create books.")
    book = Book(**book_data.model_dump())
    session.add(book)
    await session.commit()
    return book