import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from vote.models import VoteForm, Votes
from vote.views import CreateVoteView

URL_PATH = reverse("vote:create_vote")


@pytest.fixture()
def api_request(user_token: User):
    api_request = APIRequestFactory().post(URL_PATH)

    api_request.auth = user_token.auth_token
    api_request.user = user_token

    return api_request


@pytest.fixture
def create_vote_view(api_request: Request) -> CreateVoteView:
    view = CreateVoteView()
    view.setup(api_request)
    return view


@pytest.mark.django_db
def test_post(
    api_request: Request,
    vote_form: VoteForm,
    create_vote_view: CreateVoteView,
) -> None:
    vote_data = {"form": vote_form.id, "vote": 1}
    api_request.data = vote_data  # type: ignore
    create_vote_view.format_kwarg = None

    create_vote_view.post(api_request)

    votes = Votes.objects.all()
    assert len(votes) == 1
    assert votes[0].form.id == vote_form.id and votes[0].vote.id == 1
