from datetime import timedelta
from typing import Any
import pytest
from django.contrib.auth.models import User
from django.utils import timezone


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
