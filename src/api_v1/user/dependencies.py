from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.crud import get_user_by_id
from src.core.models import User
from src.utils import db_helper


async def get_user_by_id_dependency(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> User | HTTPException:
    return await get_user_by_id(user_id=user_id, session=session)
