from datetime import timedelta, datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.schemas import UserCreate, SuperUserCreate
from src.core.models import User, Profile, EmailVerificationToken, PasswordResetToken
from src.utils import hash_password, verify_password
from src.utils.auth_helpers import generate_email_verification_code, generate_password_reset_token
from src.tasks.tasks import send_verification_email, send_password_reset_token_email


async def create_user(user_data: UserCreate, session: AsyncSession) -> User | ValueError:
    user_data.password = hash_password(password=user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    profile = Profile(user_id=user.id, is_public=True)
    session.add(profile)
    await session.commit()
    return user


async def create_super_user(user_data: SuperUserCreate, session: AsyncSession) -> User | ValueError:
    user_data.password = hash_password(password=user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    profile = Profile(user_id=user.id, is_public=False)
    session.add(profile)
    await session.commit()
    return user


async def login_user(username: str, password: str, session: AsyncSession) -> User:
    statement = select(User).where(User.username == username)
    user = await session.execute(statement)
    user = user.scalar_one()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username."
        )
    if not verify_password(password=password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wrong password."
        )
    return user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | HTTPException:
    try:
        user = await session.get(User, user_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def delete_user(user: User, session: AsyncSession):
    await session.delete(user)
    await session.commit()
    return {"Your account has been deleted successfully."}


async def send_verification_email_crud(user: User, session: AsyncSession):
    if user.verified:
        return {"Your email has already been verified."}
    code = generate_email_verification_code()
    token = EmailVerificationToken(token=code, user_email=user.email)
    session.add(token)
    await session.commit()
    send_verification_email.delay(user_id=user.id, user_email=user.email, verification_token=code)
    return {"A token has been sent, please check your e-mail."}


async def verify_email_crud(token: UUID, user: User, session: AsyncSession):
    statement = select(EmailVerificationToken).where(EmailVerificationToken.user_email == user.email)
    token_db = await session.execute(statement)
    token_db = token_db.scalar_one()
    if token_db.token == token and datetime.now() - timedelta(hours=3) - token_db.created_at < timedelta(hours=1):
        user.verified = True
        user.role_access = "Verified user"
        await session.commit()
        return {"Your email has been verified successfully."}
    return {"Wrong token."}


async def send_reset_password_crud(user_email: str,
                                   session: AsyncSession):
    statement = select(User).where(User.email == user_email)
    user = await session.execute(statement)
    user = user.scalar_one()
    if user:
        reset_token = generate_password_reset_token()
        send_password_reset_token_email.delay(user_email=user_email, reset_token=reset_token)
        token = PasswordResetToken(user_email=user_email,
                                   token=reset_token)
        session.add(token)
        await session.commit()
        await session.refresh(token)
        return "Password reset token has been sent to your e-mail."
    return "Wrong e-mail."


async def reset_password_crud(reset_token: UUID,
                              new_password: str,
                              session: AsyncSession):
    try:
        statement = select(PasswordResetToken).where(PasswordResetToken.token == reset_token)
        token = await session.execute(statement)
        token = token.scalar_one()
        user_statement = select(User).where(User.email == token.user_email)
        user = await session.execute(user_statement)
        user = user.scalar_one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong token")
    if datetime.now() - timedelta(hours=3) - token.created_at > timedelta(hours=1):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your token has expired.")
    user.password = hash_password(password=new_password)
    await session.commit()
    return {"Your password has been changed."}



