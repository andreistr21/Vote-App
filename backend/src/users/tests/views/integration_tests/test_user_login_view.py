import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from conftest import user_data

from users.serializers import UserLoginSerializer, UserSerializer
from users.views import UserLoginView


@pytest.fixture()
def api_request():
    return APIRequestFactory().post(reverse("users:login"))


@pytest.fixture
def view(api_request: Request):
    view = UserLoginView()
    view.setup(api_request)
    return view


@pytest.mark.django_db
def test__get_already_logged_in_response_returned_data(
    view: UserLoginView, user: User
):
    response = view._get_already_logged_in_response(user)

    expected_response_data = json.dumps(
        {
            "detail": "You are already logged in.",
            "user": UserSerializer(user).data,
        }
    )
    assert response.data == expected_response_data
    assert response.status_code == 200


@pytest.mark.django_db
def test__get_successful_login_response(
    view: UserLoginView,
    user_token: User,
    user_data: dict[str, str],
):
    serializer = UserLoginSerializer(data={**user_data})
    serializer.is_valid()

    response = view._get_successful_login_response(serializer)

    expected_response_data = json.dumps(
        {
            "detail": "Login successful.",
            "user": UserSerializer(user_token).data,
            "token": user_token.auth_token.key,
        }
    )
    assert response.data == expected_response_data
    assert response.status_code == 200


def test__get_invalid_credentials_response(view: UserLoginView):
    response = view._get_invalid_credentials_response()

    expected_response_data = json.dumps({"error": "Invalid credentials"})
    assert response.data == expected_response_data
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_method_auth_user(
    api_request: Request,
    view: UserLoginView,
    user_token: User,
    mocker: MockerFixture,
):
    expected_response = "patched answer"
    mocker.patch.object(
        UserLoginView,
        "_get_already_logged_in_response",
        return_value=expected_response,
    )

    api_request.auth = user_token.auth_token
    api_request.user = user_token

    response = view.post(api_request)

    assert response == expected_response  # type: ignore


@pytest.mark.django_db
def test_post_method_not_auth_user_valid_data(
    api_request: Request,
    view: UserLoginView,
    user: User,  # User should be created, so serializer can check it
    user_data: dict[str, str],
    mocker: MockerFixture,
):
    expected_response = "patched answer"
    mocker.patch.object(
        UserLoginView,
        "_get_successful_login_response",
        return_value=expected_response,
    )

    api_request.auth = None
    api_request.data = {**user_data}  # type: ignore

    response = view.post(api_request)

    assert response == expected_response  # type: ignore


@pytest.mark.django_db
def test_post_method_not_auth_user_invalid_data(
    api_request: Request,
    view: UserLoginView,
    mocker: MockerFixture,
):
    expected_response = "patched answer"
    mocker.patch.object(
        UserLoginView,
        "_get_invalid_credentials_response",
        return_value=expected_response,
    )

    api_request.auth = None
    api_request.data = {}  # type: ignore

    response = view.post(api_request)

    assert response == expected_response  # type: ignore
