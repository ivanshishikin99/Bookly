from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.author.crud import get_author_by_id
from src.core.models import Author
from src.utils import db_helper


async def get_author_by_id_dependency(author_id: int,
                                      session: AsyncSession = Depends(db_helper.session_getter)) -> Author | HTTPException:
    try:
        author = await get_author_by_id(author_id=author_id,
                                  session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")
    return author
