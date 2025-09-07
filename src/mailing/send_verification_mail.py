import uuid

from src.mailing import send_email


def send_verification_email(user_email: str, verification_token: uuid.UUID):
    return send_email(recipient=user_email,
                      subject="Email verification",
                      body=f"Your verification code is {verification_token}. If this e-mail was sent by mistake just ignore it. The code is only valid for 60 minutes.")
