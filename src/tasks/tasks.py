from src.logger import log
from src.tasks.celery_conf import celery

from src.mailing.send_welcome_mail import send_welcome_email as send


@celery.task(bind=True, max_retries=5)
def send_welcome_email(self, user_id: int, username: str, email: str):
    try:
        log.info("Sending welcome email to user with id: %s", user_id)
        return send(username=username, email=email)
    except:
        self.retry()