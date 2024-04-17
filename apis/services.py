from datetime import datetime, timedelta
from functools import partial

import jwt
from django.contrib.auth.hashers import verify_password as _verify_password

from apis.models import User, RefreshToken


def generate_access_token(data: dict):
    return jwt.encode(data, "env_vars['JWT_SECRET']", algorithm="HS256")


def decode_access_token(token: str):
    return jwt.decode(token, "env_vars['JWT_SECRET']", algorithms=['HS256'])


def verify_password(password, hashed_password):
    return _verify_password(password, hashed_password)[0]


def get_new_refresh_token(user: User) -> RefreshToken:
    refresh_token = RefreshToken.objects.create(user=user,
                                                expires=get_refresh_token_expiration_time())
    refresh_token.save()

    return refresh_token


def _get_expiration_time(*, access_token: bool) -> datetime:
    current_time = datetime.now()
    if access_token:
        expires_delta = timedelta(seconds=30)
        return current_time + expires_delta

    expires_delta = timedelta(days=30)
    return current_time + expires_delta


get_refresh_token_expiration_time = partial(_get_expiration_time, access_token=False)
get_access_token_expiration_time = partial(_get_expiration_time, access_token=True)
