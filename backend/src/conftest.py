import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.fixture
def user_data() -> dict[str, str]:
    return {"username": "test-user", "password": "test-password"}


@pytest.fixture
def user(user_data) -> User:
    return get_user_model().objects.create_user(**user_data)


@pytest.fixture
def user_token(user: User) -> User:
    Token.objects.get_or_create(user=user)
    return user
