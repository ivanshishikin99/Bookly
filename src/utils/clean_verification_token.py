import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy import select

from src.core.config import settings
from src.core.models import EmailVerificationToken
from src.utils import db_helper


async def clean_email_verification_tokens_table(interval: int = 3600):
    logging.basicConfig(level=settings.logging_config.log_level,
                        format=settings.logging_config.log_format)
    log = logging.getLogger()
    while True:
        async with db_helper.session_maker() as session:
            statement = select(EmailVerificationToken).where(datetime.now()
                                                             - EmailVerificationToken.created_at
                                                             - timedelta(hours=3) > timedelta(hours=1))
            tokens = await session.execute(statement)
            tokens = tokens.scalars()
            for i in tokens:
                await session.delete(i)
                await session.commit()
            log.info("Verification tokens table has been cleaned.")
        await asyncio.sleep(delay=interval)