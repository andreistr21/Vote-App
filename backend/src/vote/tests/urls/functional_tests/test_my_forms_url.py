import pytest
from django.urls import resolve, reverse
from rest_framework.test import APIClient

from vote.views import AdminVoteFormsListView

URL_PATH = reverse("vote:my_forms")


@pytest.mark.django_db
def test_not_auth_user(api_client: APIClient):
    response = api_client.post(URL_PATH)

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_method_auth_user(auth_api_client: APIClient):
    response = auth_api_client.get(URL_PATH)

    assert response.status_code == 200


@pytest.mark.parametrize("path", [URL_PATH, "/vote/my-forms/"])
def test_view_used(path: str):
    view_class = resolve(path=path).func.view_class  # type: ignore
    assert view_class == AdminVoteFormsListView


def test_url_name():
    path = reverse("vote:my_forms")

    assert path == "/vote/my-forms/"
