from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.profile.crud import get_profile_by_id
from src.core.models import Profile
from src.utils import db_helper


async def get_profile_by_id_dependency(profile_id: int, session: AsyncSession = Depends(db_helper)) -> Profile | HTTPException:
    try:
        user = await get_profile_by_id(profile_id=profile_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user
