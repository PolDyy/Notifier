import hashlib
import json
import random
import string

from django.core.cache import cache


def generate_random_string():
    characters = string.ascii_letters + string.digits

    random_string = ''.join(
        random.choice(characters) for _ in range(16)
    )
    return random_string


def generate_hash(key_word: str):
    unique_hash = hashlib.sha256(
        (key_word + generate_random_string()).encode(),
        ).hexdigest()
    cache.set(unique_hash, True)
    return unique_hash


def generate_hash_close_channel(email: str, chat_hash: str):
    unique_hash = hashlib.sha256(
        (email + generate_random_string()).encode(),
        ).hexdigest()
    data_dict = {
        'email': email,
        'chat_hash': chat_hash
    }
    cache.set(unique_hash, json.dumps(data_dict))
    return unique_hash


def generate_hash_for_login(email: str):
    unique_hash = hashlib.sha256(
        (email + generate_random_string()).encode(),
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
