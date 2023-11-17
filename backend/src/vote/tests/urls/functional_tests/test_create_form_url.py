from typing import Any

import pytest
from django.urls import resolve, reverse
from rest_framework.test import APIClient

from vote.views import MakeVoteView

URL_PATH = reverse("vote:create_form")


@pytest.mark.django_db
def test_not_auth_user(api_client: APIClient):
    response = api_client.post(URL_PATH)

    assert response.status_code == 401


@pytest.mark.django_db
def test_post_method_auth_user(
    auth_api_client: APIClient,
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
):
    response = auth_api_client.post(
        URL_PATH, data=vote_form_data | vote_fields_data, format="json"
    )

    assert response.status_code == 200


@pytest.mark.parametrize("path", [URL_PATH, "/vote/create-form/"])
def test_view_used(path: str):
    view_class = resolve(path=path).func.view_class  # type: ignore
    assert view_class == MakeVoteView


def test_url_name():
    path = reverse("vote:create_form")

    assert path == "/vote/create-form/"
