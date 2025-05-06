import smtplib

from email.mime.text import MIMEText

from core.config import config as cfg


class Mail:
    def __init__(
        self,
        host: str = cfg.email.HOST,
        host_user: str = cfg.email.USER,
        port: int = cfg.email.PORT,
        password: str = cfg.email.PASSWORD,
    ):
        self.host = host
        self.host_user = host_user
        self.port = port
        self.password = password

    def send_email(self, email: str, message: str, subject: str):
        """Email the user"""
        message = MIMEText(message)
        message["Subject"] = subject
        message["From"] = self.host_user
        message["To"] = email
        with smtplib.SMTP_SSL(self.host, self.port) as server:
            server.login(self.host_user, self.password)
            server.sendmail(self.host_user, email, message.as_string())
