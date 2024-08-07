from abc import ABC, abstractmethod
from django.core.mail import EmailMessage, get_connection


class SendEmailABC(ABC):

    @abstractmethod
    def send(self, subject, email_from, recipient_list, message):
        pass


class SendEmail(SendEmailABC):

    def __init__(self, host: str, port: str, username: str, password: str, use_tls: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send(self, subject: str, email_from: str, to_email: list, message: str,):
        with get_connection(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=self.use_tls
        ) as connection:
            EmailMessage(subject, message, email_from,
                         to_email, connection=connection).send()
