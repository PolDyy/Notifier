import hashlib
import json
from django.conf import settings

from django.core.cache import cache


def generate_hash(key_word: str):
    unique_hash = hashlib.sha256(
        (key_word + settings.SECRET_KEY).encode(),
        ).hexdigest()
    cache.set(unique_hash, True)
    return unique_hash


def generate_hash_close_channel(email: str, chat_hash: str):
    unique_hash = hashlib.sha256(
        (email + settings.SECRET_KEY).encode(),
        ).hexdigest()
    data_dict = {
        'email': email,
        'chat_hash': chat_hash
    }
    cache.set(unique_hash, json.dumps(data_dict))
    return unique_hash


def generate_hash_for_login(email: str):
    unique_hash = hashlib.sha256(
        (email + settings.SECRET_KEY).encode(),
    ).hexdigest()
    cache.set(unique_hash, email)
    return unique_hash


def get_hash_value(unique_hash: str):
    """"""
    value = cache.get(unique_hash)
    return value


def pop_hash_value(unique_hash: str):
    value = cache.get(unique_hash)
    if value:
        cache.delete(unique_hash)
    return value
