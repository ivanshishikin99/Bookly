import uuid

from src.mailing import send_email


def send_password_reset_email(user_email: str, reset_token: uuid.UUID):
    return send_email(recipient=user_email,
                      subject="Email verification",
                      body=f"Your password reset token is {reset_token}. If this e-mail was sent by mistake just ignore it. The token is only valid for 60 minutes.")
