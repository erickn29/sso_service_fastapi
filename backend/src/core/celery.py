from celery import Celery

from core.config import config
from utils.mail import mail_service


celery_app = Celery(
    main="worker",
    broker=config.redis.url_broker,
    backend=config.redis.url_backend,
)

celery_app.conf.update(broker_connection_retry_on_startup=True)


@celery_app.task
def send_email_task(email: str, message: str, subject: str):
    mail_service.send_email(email, message, subject)
