import json
from datetime import timedelta
from typing import Any

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from vote.views import MakeVoteView


@pytest.fixture
def vote_form_data(user_token: User) -> dict[str, Any]:
    return {
        "admin": user_token.id,
        "name": "test-form-name",
        "closing": timezone.now() + timedelta(1),
    }


@pytest.fixture
def vote_fields_data() -> dict[str, list[dict[str, str]]]:
    return {
        "vote_fields": [
            {"name": "test-vote-name-1"},
            {"name": "test-vote-name-2"},
        ]
    }


@pytest.fixture()
def api_request():
    return APIRequestFactory().post(reverse("vote:create_form"))


@pytest.fixture
def view(api_request: Request):
    view = MakeVoteView()
    view.setup(api_request)
    return view


@pytest.mark.django_db
def test_post_method_valid_data(
    api_request: Request,
    view: MakeVoteView,
    user_token: User,
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
):
    api_request.auth = user_token.auth_token
    api_request.user = user_token
    api_request.data = vote_form_data | vote_fields_data  # type: ignore

    response = view.post(api_request)

    assert response.data == json.dumps(
        {"details": "Form created successfully."}
    )


@pytest.mark.django_db
def test_post_method_invalid_data(
    api_request: Request,
    view: MakeVoteView,
    user_token: User,
    vote_form_data: dict[str, Any],
):
    api_request.auth = user_token.auth_token
    api_request.user = user_token
    api_request.data = vote_form_data  # type: ignore

    response = view.post(api_request)

    assert "errors" in response.data
    assert response.status_code == 400
