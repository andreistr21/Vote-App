import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from rest_framework.test import APIClient

from users.views import UserLoginView

URL_PATH = reverse("users:login")


@pytest.mark.django_db
def test_not_auth_user(
    api_client: APIClient, user_token: User, user_data: dict[str, str]
):
    response = api_client.post(URL_PATH, data={**user_data})

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_method_response_data_auth_user(
    auth_api_client: APIClient, user_data: dict[str, str]
):
    response = auth_api_client.post(URL_PATH, data={**user_data})

    assert response.status_code == 200


@pytest.mark.parametrize("path", [URL_PATH, "/user/login/"])
def test_view_used(path: str):
    view_class = resolve(path).func.view_class  # type: ignore
    assert view_class == UserLoginView


def test_url_name():
    path = reverse("users:login")

    assert path == "/user/login/"
