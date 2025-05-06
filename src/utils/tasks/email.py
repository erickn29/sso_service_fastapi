from core.celery import celery_app


@celery_app.task
def send_email(email: str, message: str, subject: str):
    from utils.mail import mail_service

    mail_service.send_email(email, message, subject)
