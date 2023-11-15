import datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from vote.models import VoteForm


def closing_date() -> datetime.datetime:
    return timezone.now() + datetime.timedelta(days=1)


@pytest.fixture
def vote_form(user: User) -> VoteForm:
    return VoteForm.objects.create(
        admin=user,
        name="test-form-name",
        closing=closing_date(),
    )
