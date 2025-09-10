from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.author.schemas import AuthorCreate
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