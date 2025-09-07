from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.profile.crud import update_profile_partial, update_profile_full
from src.api_v1.profile.schemas import ProfileRead, ProfileUpdatePartial, ProfileUpdateFull
from src.core.models import Profile
from src.utils import db_helper
from src.utils.auth_helpers import get_profile_by_token

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def get_your_profile_view(profile: Profile = Depends(get_profile_by_token)) -> Profile:
    return profile


@router.patch("/update", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def update_your_profile_partial_view(profile_data: ProfileUpdatePartial, profile: Profile = Depends(get_profile_by_token),
                                           session: AsyncSession = Depends(db_helper.session_getter)) -> Profile:
    return await update_profile_partial(profile=profile, profile_data=profile_data, session=session)


@router.put("/update", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def update_your_profile_full_view(profile_data: ProfileUpdateFull, profile: Profile = Depends(get_profile_by_token),
                                        session: AsyncSession = Depends(db_helper.session_getter)) -> Profile:
    return await update_profile_full(profile=profile, profile_data=profile_data, session=session)
