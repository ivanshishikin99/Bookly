import smtplib
from email.message import EmailMessage

from src.core.config import settings


def send_email(recipient: str, subject: str, body: str):
    admin_email = settings.mail_config.admin_email
    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        host=settings.mail_config.hostname, port=settings.mail_config.port
    ) as server:
        server.send_message(message)
