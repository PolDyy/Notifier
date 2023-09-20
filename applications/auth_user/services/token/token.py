import datetime

import jwt
from django.conf import settings


def generate_access_token(email: str) -> str:
    """Функция генерации access токена."""
    access_token_payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + settings.ACCESS_TOKEN_LIFETIME,
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY,
        algorithm='HS256',
    )
    return access_token


def generate_refresh_token(email: str) -> str:
    """Функция генерации refresh токена."""
    refresh_token_payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + settings.REFRESH_TOKEN_LIFETIME,
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return refresh_token


def get_jwt_payload(token: str) -> None | dict:
    try:
        payload_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        return None
    return payload_jwt
