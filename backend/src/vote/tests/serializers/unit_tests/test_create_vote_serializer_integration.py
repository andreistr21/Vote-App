from typing import Any

import pytest
from pytest_mock import MockerFixture
from rest_framework.serializers import ValidationError

from vote.models import VoteFields, VoteForm, Votes
from vote.serializers import CreateVotesSerializer


@pytest.mark.django_db
class TestOnlyOneVotePerUserValidation:
    def test_no_votes(self, mocker: MockerFixture) -> None:
        request = mocker.Mock()
        request.user.id = 11
        context = {"request": request}

        vote_fields = mocker.Mock()
        vote_fields.form.id = 15

        create_vote_serializer = CreateVotesSerializer(
            data={}, context=context
        )

        create_vote_serializer.only_one_vote_per_user_validation(vote_fields)

    def test_with_votes(
        self, mocker: MockerFixture, vote_form_data_user: dict[str, Any]
    ) -> None:
        request = mocker.Mock()
        request.user.id = vote_form_data_user["admin"].id
        context = {"request": request}

        vote_form = VoteForm.objects.create(**vote_form_data_user)

        vote_fields_data = mocker.Mock()
        vote_field = VoteFields.objects.create(
            form=vote_form, name="test-name"
        )
        vote_fields_data.form.id = vote_form.id

        Votes.objects.create(
            user=vote_form_data_user["admin"], form=vote_form, vote=vote_field
        )

        create_vote_serializer = CreateVotesSerializer(
            data={}, context=context
        )

        with pytest.raises(ValidationError) as e:
            create_vote_serializer.only_one_vote_per_user_validation(
                vote_fields_data
            )

        assert (
            e.value.args[0]["errors"]["vote"]
            == "User already voted for this form. Delete previous vote if you"
            " want to change it."
        )


@pytest.mark.django_db
class TestOnlyOneVotePerFieldPerUser:
    def test_no_votes(self, mocker: MockerFixture) -> None:
        request = mocker.Mock()
        request.user.id = 11
        context = {"request": request}

        vote_fields = mocker.Mock()
        vote_fields.id = 15

        create_vote_serializer = CreateVotesSerializer(
            data={}, context=context
        )

        create_vote_serializer.only_one_vote_per_field_per_user(vote_fields)

    def test_with_votes(
        self, mocker: MockerFixture, vote_form_data_user: dict[str, Any]
    ) -> None:
        request = mocker.Mock()
        request.user.id = vote_form_data_user["admin"].id
        context = {"request": request}

        vote_form = VoteForm.objects.create(**vote_form_data_user)

        vote_fields_data = mocker.Mock()
        vote_field = VoteFields.objects.create(
            form=vote_form, name="test-name"
        )
        vote_fields_data.id = vote_form.id

        Votes.objects.create(
            user=vote_form_data_user["admin"], form=vote_form, vote=vote_field
        )

        create_vote_serializer = CreateVotesSerializer(
            data={}, context=context
        )

        with pytest.raises(ValidationError) as e:
            create_vote_serializer.only_one_vote_per_field_per_user(
                vote_fields_data
            )

        assert (
            e.value.args[0]["errors"]["vote"]
            == "User already voted for this field. Delete previous vote if you"
            " want to change it."
        )
