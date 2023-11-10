import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



@pytest.fixture
def user() -> User:
    return get_user_model().objects.create_user(
        username="test-user", password="test-password"
    )


@pytest.fixture
def user_token(user:User) -> User:
    Token.objects.get_or_create(user=user)
    return user
