import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy import select

from src.core.config import settings
from src.core.models import PasswordResetToken
from src.utils import db_helper


async def clean_password_reset_tokens_table(interval: int = 3600):
    logging.basicConfig(level=settings.logging_config.log_level,
                        format=settings.logging_config.log_format)
    log = logging.getLogger()
    while True:
        async with db_helper.session_maker() as session:
            statement = select(PasswordResetToken).where(datetime.now()
                                                         - PasswordResetToken.created_at
                                                         - timedelta(hours=3) > timedelta(hours=1))
            tokens = await session.execute(statement)
            tokens = tokens.scalars()
            for i in tokens:
                await session.delete(i)
                await session.commit()
            log.info("Password reset tokens table has been cleaned.")
            await asyncio.sleep(delay=interval)