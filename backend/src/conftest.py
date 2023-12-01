from typing import Callable

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def auth_api_client(api_client: APIClient, user_token: User) -> APIClient:
    api_client.force_authenticate(user_token)
    return api_client


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


@pytest.fixture
def user_gen() -> Callable[[str], User]:
    def _create_user(username: str, password="test-password") -> User:
        return get_user_model().objects.create_user(
            username=username, password=password
        )

    return _create_user
