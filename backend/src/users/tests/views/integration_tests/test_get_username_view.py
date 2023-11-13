import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from users.views import GetUsernameView


@pytest.mark.django_db
def test_get_response(user_token: User, user_data: dict[str, str]):
    request = APIRequestFactory().get(reverse("users:get_username"))
    request.user = user_token

    view = GetUsernameView()
    view.setup(request)

    response = view.get(request)

    assert response.data == json.dumps({"username": user_data["username"]})
