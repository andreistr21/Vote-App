from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from vote.models import VoteForm


def closing_date():
    return timezone.now() + timedelta(days=1)


@pytest.mark.django_db
class TestFieldsChoices:
    """
    Tests choices of statistics_type and votes_type fields.
    """

    statistics_type_valid_choices = [1, 2]
    statistics_type_invalid_choices = [0, 3]

    votes_type_valid_choices = [1, 2]
    votes_type_invalid_choices = [0, 3]

    @pytest.mark.parametrize(
        "statistics_choice", statistics_type_valid_choices
    )
    def test_valid_statistics_type_choices(
        self, statistics_choice: int, user: User
    ):
        form = VoteForm(
            admin=user,
            name="test-name",
            statistics_type=statistics_choice,
            closing=closing_date(),
        )

        form.full_clean()

        assert form.statistics_type == statistics_choice

    @pytest.mark.parametrize("votes_choice", votes_type_valid_choices)
    def test_valid_votes_type_choices(self, votes_choice: int, user: User):
        form = VoteForm(
            admin=user,
            name="test-name",
            votes_type=votes_choice,
            closing=closing_date(),
        )

        form.full_clean()

        assert form.votes_type == votes_choice

    @pytest.mark.parametrize(
        "statistics_choice", statistics_type_invalid_choices
    )
    def test_invalid_statistics_type_choices(
        self, statistics_choice: int, user: User
    ):
        form = VoteForm(
            admin=user,
            name="test-name",
            statistics_type=statistics_choice,
            closing=closing_date(),
        )

        with pytest.raises(ValidationError):
            form.full_clean()

    @pytest.mark.parametrize("votes_choice", votes_type_invalid_choices)
    def test_invalid_votes_type_choices(self, votes_choice: int, user: User):
        form = VoteForm(
            admin=user,
            name="test-name",
            votes_type=votes_choice,
            closing=closing_date(),
        )

        with pytest.raises(ValidationError):
            form.full_clean()
