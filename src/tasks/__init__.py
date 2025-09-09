__all__ = ("send_welcome_email",
           "send_verification_email",
           "send_password_reset_token_email",
           )

import logging
import sys

from src.core.config import settings

from .tasks import send_welcome_email, send_verification_email, send_password_reset_token_email

if sys.argv[0] == "worker":
    logging.basicConfig(level=logging.INFO, format=settings.logging_config.log_format)