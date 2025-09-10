from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Book


async def get_book_by_id(book_id: int,
                         session: AsyncSession) -> Book | None:
    book = await session.get(Book, book_id)
    return book
