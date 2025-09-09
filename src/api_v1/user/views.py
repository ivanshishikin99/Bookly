from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_cache.decorator import cache
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.crud import create_user, login_user, delete_user, create_super_user, send_verification_email, \
    send_verification_email_crud, verify_email_crud, send_reset_password_crud, reset_password_crud
from src.api_v1.user.dependencies import get_user_by_id_dependency
from src.api_v1.user.schemas import UserRead, UserCreate, SuperUserRead, SuperUserCreate
from src.core.models import User, EmailVerificationToken
from src.tasks import send_welcome_email
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token, TokenModel, create_access_token, create_refresh_token, \
    generate_email_verification_code

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/users/login")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user_view(user_data: UserCreate,
                             session: AsyncSession = Depends(db_helper.session_getter)) -> User | ValueError:
    user = await create_user(user_data=user_data, session=session)
    send_welcome_email.delay(username=user_data.username, email=user_data.email, user_id=user.id)
    return user


@router.post("/register_super_user", response_model=SuperUserRead, status_code=status.HTTP_201_CREATED)
async def register_super_user_view(user_data: SuperUserCreate,
                                   session: AsyncSession = Depends(db_helper.session_getter)) -> User | ValueError:
    user = await create_super_user(user_data=user_data, session=session)
    return user


@router.post("/login", response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login_user_view(response: Response,
                          login_data: OAuth2PasswordRequestForm = Depends(),
                          session: AsyncSession = Depends(db_helper.session_getter)) -> TokenModel:
    user = await login_user(username=login_data.username, password=login_data.password,
                            session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return TokenModel(access_token=access_token, refresh_token=refresh_token)


@router.get("/send_verification_email", status_code=status.HTTP_200_OK)
async def send_verification_email_view(user: User = Depends(get_user_by_token),
                                       session: AsyncSession = Depends(db_helper.session_getter)):
    return await send_verification_email_crud(user=user, session=session)


@router.post("/verify_email", status_code=status.HTTP_200_OK)
async def verify_email_view(token: UUID,
                            user: User = Depends(get_user_by_token),
                            session: AsyncSession = Depends(db_helper.session_getter)):
    return await verify_email_crud(token=token, user=user, session=session)


@router.post("/send_password_reset_token", status_code=status.HTTP_200_OK)
async def send_reset_password_view(user_email: str,
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await send_reset_password_crud(user_email=user_email, session=session)


@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password_view(reset_token: UUID,
                              new_password: SecretStr,
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await reset_password_crud(reset_token=reset_token,
                                     new_password=new_password.get_secret_value(),
                                     session=session)


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
@cache(expire=60)
async def get_user_by_id_view(user: User = Depends(get_user_by_id_dependency)) -> User | HTTPException:
    return user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(response: Response,
                           user: User = Depends(get_user_by_token),
                           session: AsyncSession = Depends(db_helper.session_getter)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return await delete_user(user=user, session=session)