from datetime import timedelta
from time import sleep
from typing import Callable

import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from vote.models import VoteForm
from vote.serializers import VoteFormSerializer

URL_PATH = reverse("vote:my_forms")


@pytest.fixture()
def api_request(user_token: User):
    api_request = APIRequestFactory().get(URL_PATH)

    api_request.auth = user_token.auth_token
    api_request.user = user_token

    return api_request


def vote_form_gen(user: User, amount: int) -> list[VoteForm]:
    forms_list = []
    for i in range(amount):
        forms_list.append(
            VoteForm.objects.create(
                admin=user,
                name=f"test-name-{i}-{user.username}",
                closing=timezone.now() + timedelta(1),
            )
        )
        sleep(0.001)

    return forms_list


def _inner_querysets_to_list(data):
    for item in data:
        for key in item.keys():
            if type(item[key]) is QuerySet:
                item[key] = list(item[key])


@pytest.mark.django_db
def test_filter_by_user(
    auth_api_client: APIClient,
    api_request: Request,
    user_token: User,
    user_gen: Callable[[str], User],
):
    admin_forms = vote_form_gen(user_token, 7)
    user_1 = user_gen("test-user-1")
    vote_form_gen(user_1, 5)

    response = auth_api_client.get(URL_PATH, format="json")

    admin_forms = admin_forms[::-1]
    resp_forms = response.data["results"]
    serialized_admin_forms = VoteFormSerializer(
        instance=admin_forms,
        context={"request": api_request},
        many=True,
    ).data
    _inner_querysets_to_list(serialized_admin_forms)
    _inner_querysets_to_list(resp_forms)
    assert len(response.data["results"]) == 7
    assert resp_forms == serialized_admin_forms


@pytest.mark.django_db
def test_page_size(auth_api_client: APIClient, user_token: User):
    vote_form_gen(user_token, 16)

    response = auth_api_client.get(URL_PATH, format="json")

    assert len(response.data["results"]) == 10
