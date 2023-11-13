import json

import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from rest_framework.test import APIClient

from users.views import GetUsernameView

URL_PATH = reverse("users:get_username")


@pytest.mark.django_db
def test_not_auth_user(api_client: APIClient):
    response = api_client.get(URL_PATH)

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_method_response_data_auth_user(
    auth_api_client: APIClient, user_token: User
):
    response = auth_api_client.get(URL_PATH)

    expected_response_data = json.dumps({"username": user_token.username})
    assert response.data == expected_response_data


@pytest.mark.parametrize("path", [URL_PATH, "/user/get-username/"])
def test_view_used(path: str):
    view_class = resolve(path).func.view_class  # type: ignore
    assert view_class == GetUsernameView


def test_url_name():
    path = reverse("users:get_username")

    assert path == "/user/get-username/"
