from rest_framework.authtoken.models import Token


def get_token_by_key(key: str) -> Token | None:
    return Token.objects.filter(key=key).first()
