from datetime import timedelta
from typing import Any

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from vote.models import VoteFields, VoteForm, Votes
from vote.serializers import VoteFormSerializer


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


@pytest.fixture
def vote_form(
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
) -> VoteForm | None:
    serializer = VoteFormSerializer(data=vote_form_data | vote_fields_data)
    return serializer.save() if serializer.is_valid() else None


@pytest.fixture
def vote_form_with_vote(vote_form: VoteForm) -> VoteForm | None:
    if vote_form:
        Votes.objects.create(
            user=vote_form.admin,
            form=vote_form,
            vote=VoteFields.objects.all()[1],
        )
        return vote_form
    return None
