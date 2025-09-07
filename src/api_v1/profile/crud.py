from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.profile.schemas import ProfileUpdatePartial, ProfileUpdateFull
from src.core.models import Profile


async def update_profile_partial(profile: Profile, profile_data: ProfileUpdatePartial, session: AsyncSession) -> Profile:
    for k, v in profile_data.model_dump().items():
        if k:
            setattr(profile, k, v)
    await session.commit()
    return profile


async def update_profile_full(profile: Profile, profile_data: ProfileUpdateFull, session: AsyncSession) -> Profile:
    for k, v in profile_data.model_dump().items():
        setattr(profile, k, v)
    await session.commit()
    return profile


async def get_profile_by_id(profile_id: int, session: AsyncSession) -> Profile | None:
    profile = await session.get(Profile, profile_id)
    return profile
