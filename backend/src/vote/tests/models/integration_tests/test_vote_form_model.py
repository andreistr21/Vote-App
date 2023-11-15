from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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


@pytest.mark.django_db
class TestClosingGreaterThanCreatedConstraint:
    """
    Tests that closing_greater_than_created constraint works as expected.
    """

    def test_valid_closing_date(self, user: User):
        closing_date_var = closing_date()
        form = VoteForm(
            admin=user,
            name="test-name",
            closing=closing_date_var,
        )

        form.full_clean()
        form.save()

        assert form.closing == closing_date_var

    def test_invalid_closing_date(self, user: User):
        form = VoteForm(
            admin=user,
            name="test-name",
            closing=timezone.now() - timedelta(days=1),
        )

        with pytest.raises(IntegrityError):
            form.save()


@pytest.mark.django_db
class TestDunderMethods:
    def test_str(self, user: User):
        form_name = "check-test-name"
        form = VoteForm(
            admin=user,
            name=form_name,
            closing=closing_date(),
        )
        form.save()

        assert str(form) == f"Form: {form_name}"


# Fields constraints

@pytest.mark.django_db
class TestNameConstraints:
    def test_max_length_allowed(self, user: User):
        name = "ten-chars-" * 15
        form = VoteForm(
            admin=user,
            name=name,
            closing=closing_date(),
        )

        form.full_clean()
        form.save()

        assert form.name == name

    def test_max_length_forbidden(self, user: User):
        name = "ten-chars-" * 15 + "c"
        form = VoteForm(
            admin=user,
            name=name,
            closing=closing_date(),
        )

        with pytest.raises(ValidationError) as e:
            form.full_clean()
            form.save()
            
            assert (
                e["name"]  # type: ignore
                == "Ensure this value has at most 150 characters (it has 151)."
            )
