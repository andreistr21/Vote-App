import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from vote.models import VoteForm
from vote.views import DeleteVoteView

URL_PATH = reverse("vote:delete_vote")


@pytest.fixture()
def api_request(user_token: User) -> Request:
    api_request = APIRequestFactory().post(URL_PATH)

    api_request.auth = user_token.auth_token
    api_request.user = user_token

    return api_request


@pytest.fixture
def delete_vote_view(api_request: Request) -> DeleteVoteView:
    view = DeleteVoteView()
    view.setup(api_request)
    return view


@pytest.mark.django_db
def test_get_queryset(
    delete_vote_view: DeleteVoteView,
    vote_form_with_vote: VoteForm,
) -> None:
    form_votes = vote_form_with_vote.votes.all()

    queryset = delete_vote_view.get_queryset()

    assert list(form_votes) == list(queryset)


@pytest.mark.django_db
def test_get_object_success(
    mocker: MockerFixture,
    auth_api_client: APIClient,
    vote_form_with_vote: VoteForm,
) -> None:
    mock_request = mocker.Mock()
    data = {"user": vote_form_with_vote.admin.id, "vote": 2}
    mock_request.user.id = data["user"]
    mock_request.data = data["vote"]

    response = auth_api_client.delete(URL_PATH, data)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_get_object_not_found(
    mocker: MockerFixture, auth_api_client: APIClient, vote_form: VoteForm
) -> None:
    mock_request = mocker.Mock()
    data = {"user": vote_form.admin.id, "vote": 2}
    mock_request.user.id = data["user"]
    mock_request.data = data["vote"]

    response = auth_api_client.delete(URL_PATH, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
