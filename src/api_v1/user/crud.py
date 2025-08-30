from fastapi import HTTPException, status
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


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | HTTPException:
    try:
        user = await session.get(User, user_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


