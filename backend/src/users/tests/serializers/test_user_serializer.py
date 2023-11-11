import pytest
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer


@pytest.fixture
def user_data():
    return {"id": 1, "username": "test_user"}


@pytest.fixture
def test_user(user_data):
    return get_user_model().objects.create(**user_data)


@pytest.mark.django_db
def test_serialization(test_user):
    serializer = UserSerializer(instance=test_user)
    expected_data = {"id": 1, "username": "test_user"}
    assert serializer.data == expected_data
