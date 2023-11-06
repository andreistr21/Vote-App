from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def get_token_by_key(key: str) -> Token | None:
    return Token.objects.filter(key=key).first()


def get_or_create_token_by_user(user: User) -> Token:
    return Token.objects.get_or_create(user=user)[0]
