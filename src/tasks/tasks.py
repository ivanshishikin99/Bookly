from uuid import UUID

from src.logger import log
from src.tasks.celery_conf import celery

from src.mailing.send_welcome_mail import send_welcome_email as send
from src.mailing.send_verification_mail import send_verification_email as send_verif


@celery.task(bind=True, max_retries=5)
def send_welcome_email(self, user_id: int, username: str, email: str):
    try:
        log.info("Sending welcome email to user with id: %s", user_id)
        return send(username=username, email=email)
    except:
        self.retry()


@celery.task(bind=True, max_retries=5)
def send_verification_email(self, user_id: int, user_email: str, verification_token: UUID):
    try:
        log.info("Sending verification email to user with id: %s", user_id)
        return send_verif(user_email=user_email, verification_token=verification_token)
    except:
        self.retry()