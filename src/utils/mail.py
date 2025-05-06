import smtplib

from email.mime.text import MIMEText

from core.config import config


class Mail:
    def __init__(
        self,
        host: str = config.email.host,
        host_user: str = config.email.user,
        port: int = config.email.port,
        password: str = config.email.password,
    ):
        self.host = host
        self.host_user = host_user
        self.port = port
        self.password = password

    def send_email(self, email: str, message: str, subject: str):
        """Email the user"""
        message_ = MIMEText(message)
        message_["Subject"] = subject
        message_["From"] = self.host_user
        message_["To"] = email
        with smtplib.SMTP_SSL(self.host, self.port) as server:
            server.login(self.host_user, self.password)
            server.sendmail(self.host_user, email, message_.as_string())


mail_service = Mail()
