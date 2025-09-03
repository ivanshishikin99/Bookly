from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.crud import create_user, login_user
from src.api_v1.user.dependencies import get_user_by_id_dependency
from src.api_v1.user.schemas import UserRead, UserCreate
from src.core.models import User
from src.mailing import send_welcome_email
from src.utils import db_helper, create_access_token, create_refresh_token

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/users/login")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_200_OK)
async def register_user_view(user_data: UserCreate,
                           session: AsyncSession = Depends(db_helper.session_getter)) -> User | ValueError:
    send_welcome_email(username=user_data.username, email=user_data.email)
    return await create_user(user_data=user_data, session=session)


@router.post("/login", response_model=UserRead, status_code=status.HTTP_200_OK)
async def login_user_view(response: Response,
                          login_data: OAuth2PasswordRequestForm = Depends(),
                          session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await login_user(username=login_data.username, password=login_data.password,
                            session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return user


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_id_view(user: User = Depends(get_user_by_id_dependency)) -> User | HTTPException:
    return user
