from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.crud import create_user
from src.api_v1.user.dependencies import get_user_by_id_dependency
from src.api_v1.user.schemas import UserRead, UserCreate
from src.core.models import User
from src.utils import db_helper

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserRead, status_code=status.HTTP_200_OK)
async def create_user_view(user_data: UserCreate,
                           session: AsyncSession = Depends(db_helper.session_getter)) -> User | ValueError:
    return await create_user(user_data=user_data, session=session)


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_id_view(user: User = Depends(get_user_by_id_dependency)) -> User | HTTPException:
    return user
