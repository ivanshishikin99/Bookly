from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.review.crud import get_review_by_id
from src.core.models import Review
from src.utils import db_helper


async def get_review_by_id_dependency(review_id: int,
                                      session: AsyncSession = Depends(db_helper.session_getter)) -> Review | HTTPException:
    return await get_review_by_id(review_id=review_id,
                                  session=session)