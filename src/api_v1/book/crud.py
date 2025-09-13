from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.book.schemas import BookCreate, BookUpdatePartial, BookUpdateFull, BookRead
from src.core.models import Book, User, Author, Review


async def get_book_by_id(book_id: int,
                         session: AsyncSession) -> Book | None:
    book = await session.get(Book, book_id)
    return book


async def create_book(book_data: BookCreate,
                      user: User,
                      session: AsyncSession) -> Book | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to create books.")
    book = Book(**book_data.model_dump())
    session.add(book)
    await session.commit()
    return book


async def update_book_partial(book_data: BookUpdatePartial,
                              user: User,
                              book: Book,
                              session: AsyncSession) -> Book | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to modify books.")
    for k, v in book_data.model_dump().items():
        if k:
            setattr(book, k, v)
    await session.commit()
    return book


async def update_book_full(book_data: BookUpdateFull,
                           user: User,
                           book: Book,
                           session: AsyncSession) -> Book | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to modify books.")
    for k, v in book_data.model_dump().items():
        setattr(book, k, v)
    await session.commit()
    return book


async def delete_book(user: User,
                      book: Book,
                      session: AsyncSession):
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to delete books.")
    await session.delete(book)
    await session.commit()
    return {"Book deleted successfully."}


async def get_books_by_author(author: Author,
                              session: AsyncSession) -> list[BookRead]:
    statement = select(Book).where(Book.author == author)
    books = await session.execute(statement)
    books = books.scalars()
    books_read = list()
    for book in books:
        books_read.append(BookRead(title=book.title,
                                   year_of_release=book.year_of_release,
                                   author=book.author.full_name,
                                   description=book.description))
    return books_read


async def get_book_reviews(book: Book,
                           session: AsyncSession) -> Sequence[Review] | None:
    statement = select(Review).where(Review.book_id == book.id)
    reviews = await session.execute(statement)
    reviews = reviews.scalars().all()
    return reviews

