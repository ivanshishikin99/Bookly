from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.author.schemas import AuthorCreate, AuthorUpdatePartial, AuthorUpdateFull
from src.core.models import User, Author


async def create_author(author_data: AuthorCreate,
                        user: User,
                        session: AsyncSession) -> Author | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to create authors.")
    author = Author(**author_data.model_dump())
    session.add(author)
    await session.commit()
    return author


async def get_author_by_id(author_id: int,
                           session: AsyncSession) -> Author | None:
    author = await session.get(Author, author_id)
    return author


async def update_author_partial(author_data: AuthorUpdatePartial,
                                user: User,
                                author: Author,
                                session: AsyncSession) -> Author | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to modify authors.")
    for k, v in author_data.model_dump().items():
        if k:
            setattr(author, k, v)
    await session.commit()
    return author


async def update_author_full(author_data: AuthorUpdateFull,
                             user: User,
                             author: Author,
                             session: AsyncSession) -> Author | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to modify authors.")
    for k, v in author_data.model_dump().items():
        setattr(author, k, v)
    await session.commit()
    return author


async def delete_author(user: User,
                        author: Author,
                        session: AsyncSession):
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to delete authors.")
    await session.delete(author)
    await session.commit()
    return {"Author has been deleted successfully."}