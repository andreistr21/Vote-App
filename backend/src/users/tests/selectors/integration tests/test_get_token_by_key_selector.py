import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from users.selectors import get_token_by_key


@pytest.mark.django_db
def test_no_token_exists():
    result = get_token_by_key("unexistent-token-key")

    assert result is None


@pytest.mark.django_db
def test_token_exists(user_token: User):
    result = get_token_by_key(user_token.auth_token.key)

    assert result == user_token.auth_token
