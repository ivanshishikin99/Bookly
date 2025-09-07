from fastapi import APIRouter, status, Depends

from src.api_v1.profile.schemas import ProfileRead
from src.core.models import User, Profile
from src.utils import db_helper
from src.utils.auth_helpers import get_profile_by_token

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def get_your_profile_view(profile: Profile = Depends(get_profile_by_token)) -> Profile:
    return profile
