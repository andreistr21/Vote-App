import datetime

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from vote.models import VoteFields, VoteForm


def closing_date() -> datetime.datetime:
    return timezone.now() + datetime.timedelta(days=1)


@pytest.fixture
def vote_form(user: User) -> VoteForm:
    return VoteForm.objects.create(
        admin=user,
        name="test-form-name",
        closing=closing_date(),
    )


@pytest.mark.django_db
class TestDunderMethods:
    def test_str(self, vote_form: VoteForm):
        vote_field = VoteFields.objects.create(
            form=vote_form,
            name="test-field-name",
        )

        assert (
            str(vote_field)
            == f"Vote fields: {vote_field.form} — test-form-name"
        )
