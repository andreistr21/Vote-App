import datetime
from pydoc import describe
from django.forms import ValidationError

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


@pytest.mark.django_db
class TestNameConstraints:
    def test_max_length_allowed(self, vote_form: VoteForm):
        name = "ten-chars-" * 8
        vote_field = VoteFields.objects.create(
            form=vote_form,
            name=name,
        )

        vote_field.full_clean()
        vote_field.save()

        assert vote_field.name == name

    def test_max_length_forbidden(self, vote_form: VoteForm):
        name = "ten-chars-" * 8 + "c"
        vote_field = VoteFields.objects.create(
            form=vote_form,
            name=name,
        )

        with pytest.raises(ValidationError):
            vote_field.full_clean()


@pytest.mark.django_db
class TestDescriptionConstraints:
    def test_description_provided(self, vote_form: VoteForm):
        vote_field = VoteFields.objects.create(
            form=vote_form, name="test-name", description="test-desc"
        )

        vote_field.full_clean()
        vote_field.save()

        assert vote_field.description == "test-desc"

    def test_description_not_provided(self, vote_form: VoteForm):
        vote_field = VoteFields.objects.create(
            form=vote_form, name="test-name"
        )

        vote_field.full_clean()
        vote_field.save()

        assert vote_field.description is None
