from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.models import User, Profile
from src.utils import encode_jwt, decode_jwt, db_helper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/users/login")


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

def create_token(payload: dict,
                 token_type: str):
    jwt_payload = {"type": token_type}
    if token_type == "access_token":
        expire_minutes: int = settings.jwt_config.access_token_expire_minutes
    elif token_type == "refresh_token":
        expire_minutes: int = settings.jwt_config.refresh_token_expire_minutes
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
    jwt_payload.update(payload)
    return encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes)


def create_access_token(user: User) -> str:
    jwt_payload = {"sub": user.username,
                   "id": user.id,
                   "email": user.email,
                   "role_access": user.role_access,
                   "verified": user.verified}
    return create_token(payload=jwt_payload, token_type="access_token")


def create_refresh_token(user: User) -> str:
    jwt_payload = {"sub": user.username,
                   "id": user.id,
                   "email": user.email}
    return create_token(payload=jwt_payload, token_type="refresh_token")


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict | HTTPException:
    try:
        jwt = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in to view this page.")
    return jwt


async def get_user_by_token(payload: dict = Depends(get_current_token_payload),
                            session: AsyncSession = Depends(db_helper.session_getter)) -> User | HTTPException:
    token_type = payload.get("type")
    if not token_type == "access_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
    user_id = payload.get("id")
    if not (user := await session.get(User, user_id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token data.")
    return user


async def get_profile_by_token(payload: dict = Depends(get_current_token_payload),
                               session: AsyncSession = Depends(db_helper.session_getter)) -> Profile | HTTPException:
    token_type = payload.get("type")
    if not token_type == "access_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
    user_id = payload.get("id")
    if not (user := await session.get(User, user_id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token data.")
    statement = select(Profile).where(Profile.user_id == user.id)
    profile = await session.execute(statement)
    profile = profile.scalar_one()
    return profile
