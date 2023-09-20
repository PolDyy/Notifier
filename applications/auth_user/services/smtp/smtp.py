from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from applications.auth_user.services.hash.hash import generate_hash_for_login, generate_hash_close_channel


class EmailSending:
    """Класс отправки сообщений."""

    DEFAULT_CONTENT = {
        "domain": "0.0.0.0:8000",
        "protocol": "http",
    }

    @classmethod
    def send_auth_email(
        cls,
        email_to_sent: str
    ) -> None:
        """Функция отправки сообщения для входа."""

        unique_hash = generate_hash_for_login(email_to_sent)
        message_data = cls.DEFAULT_CONTENT | {'unique_hash': unique_hash}
        message = render_to_string(
            'email_auth.html',
            message_data,
        )
        print(message)
        send_mail(
            'Аутентификация',
            message,
            settings.EMAIL_HOST_USER,
            [email_to_sent],
            fail_silently=True,
        )

    @classmethod
    def send_to_channel_owner(
        cls,
        email_to_sent: str,
        user_email: str,
        channel_name: str,
        channel_hash: str
    ) -> None:
        """Функция отправки сообщения создателю канала."""
        unique_hash = generate_hash_close_channel(user_email, channel_hash)
        data = {
            'unique_hash': unique_hash,
            'user_email': user_email,
            'name': channel_name,
        }
        message_data = cls.DEFAULT_CONTENT | data
        message = render_to_string(
            'email_auth.html',
            message_data,
        )
        print(message)
        send_mail(
            'Запрос на подписку',
            message,
            settings.EMAIL_HOST_USER,
            [email_to_sent],
            fail_silently=True,
        )
