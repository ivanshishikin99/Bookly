from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.profile.schemas import ProfileUpdatePartial, ProfileUpdateFull
from src.core.models import Profile, User


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


async def get_profile_by_username(username: str, session: AsyncSession) -> Profile | None:
    statement = select(User).where(User.username == username)
    user = await session.execute(statement)
    user = user.scalar_one()
    statement = select(Profile).where(Profile.user == user)
    profile = await session.execute(statement)
    profile = profile.scalar_one()
    return profile
