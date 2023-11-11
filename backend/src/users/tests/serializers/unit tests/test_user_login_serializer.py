import pytest
from pytest_mock import MockerFixture
from django.contrib.auth.models import User

from users.serializers import UserLoginSerializer


@pytest.fixture
def authenticate_mocked(mocker: MockerFixture):
    return mocker.patch("users.serializers.authenticate")


def test_valid_credentials(authenticate_mocked):
    user_data = {"username": "existing_user", "password": "password123"}
    authenticate_mocked.return_value = User(**user_data)
    serializer = UserLoginSerializer(data=user_data)
    serializer.is_valid()
    assert serializer.is_valid()
    assert "user" in serializer.validated_data
    assert serializer.validated_data["user"].username == user_data["username"]


def test_missing_password():
    user_data = {"username": "nonexisting_user"}
    serializer = UserLoginSerializer(data=user_data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_missing_username():
    user_data = {"password": "password123"}
    serializer = UserLoginSerializer(data=user_data)
    assert not serializer.is_valid()
    assert "username" in serializer.errors


def test_invalid_credentials(authenticate_mocked):
    authenticate_mocked.return_value = None
    data = {"username": "nonexistent_user", "password": "wrong_password"}
    serializer = UserLoginSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors
    assert (
        "Access denied: wrong username or password."
        in serializer.errors["non_field_errors"]
    )
