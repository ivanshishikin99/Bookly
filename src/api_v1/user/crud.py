from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.schemas import UserCreate
from src.core.models import User
from src.utils import hash_password


async def create_user(user_data: UserCreate, session: AsyncSession) -> User | ValueError:
    user_data.password = hash_password(password=user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
