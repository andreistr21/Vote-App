import json
from datetime import timedelta
from typing import Any

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from vote.models import VoteFields, VoteForm, Votes
from vote.serializers import VoteFieldsSerializer, VoteFormSerializer

# ==================
# Creation tests
# ==================


@pytest.mark.django_db
def test_create_valid_data(
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
):
    serializer = VoteFormSerializer(data=vote_form_data | vote_fields_data)

    serializer.is_valid()
    serializer.save()

    assert VoteForm.objects.get(name=vote_form_data["name"])
    assert VoteFields.objects.get(
        name=vote_fields_data["vote_fields"][0]["name"]
    )
    assert VoteFields.objects.get(
        name=vote_fields_data["vote_fields"][1]["name"]
    )


@pytest.mark.django_db
def test_integrity_error_closing_greater_than_created(
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
):
    vote_form_data["closing"] = timezone.now() - timedelta(1)
    serializer = VoteFormSerializer(data=vote_form_data | vote_fields_data)

    serializer.is_valid()
    with pytest.raises(ValidationError):
        serializer.save()


@pytest.mark.django_db
def test_integrity_error_unknown_error(
    mocker: MockerFixture,
    vote_form_data: dict[str, Any],
    vote_fields_data: dict[str, list[dict[str, str]]],
):
    error_msg = "Unknown error message"
    mocker.patch(
        "vote.serializers.VoteForm.objects.create",
        side_effect=IntegrityError(error_msg),
    )

    vote_form_data["closing"] = timezone.now() - timedelta(1)
    serializer = VoteFormSerializer(data=vote_form_data | vote_fields_data)

    serializer.is_valid()
    with pytest.raises(ValidationError) as e:
        serializer.save()

    assert json.loads(e.value.args[0])["errors"]["Unknown error"] == error_msg


@pytest.mark.django_db
def test_create_with_only_one_vote_field(
    vote_form_data: dict[str, Any],
):
    vote_fields_data = {
        "vote_fields": [
            {"name": "test-vote-name-1"},
        ]
    }
    serializer = VoteFormSerializer(data=vote_form_data | vote_fields_data)

    assert not serializer.is_valid()
    assert "vote_fields" in serializer.errors


# ==================
# Representation tests
# ==================


@pytest.mark.django_db
def test_user_vote_id_representation_empty(
    mocker: MockerFixture, vote_form: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token

    serializer = VoteFormSerializer(
        instance=vote_form, context={"request": request_mock}
    )

    assert not list(serializer.data["user_vote_id"])


@pytest.mark.django_db
def test_user_vote_id_representation_with_value(
    mocker: MockerFixture, vote_form_with_vote: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token

    serializer = VoteFormSerializer(
        instance=vote_form_with_vote, context={"request": request_mock}
    )

    assert list(serializer.data["user_vote_id"]) == [2]


@pytest.mark.django_db
def test_votes_count_representation_zero(
    mocker: MockerFixture, vote_form: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token

    serializer = VoteFormSerializer(
        instance=vote_form, context={"request": request_mock}
    )

    assert not list(serializer.data["votes_count"])


@pytest.mark.django_db
def test_votes_count_representation_one(
    mocker: MockerFixture, vote_form_with_vote: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token

    serializer = VoteFormSerializer(
        instance=vote_form_with_vote, context={"request": request_mock}
    )

    assert len(list(serializer.data["votes_count"])) == 1


@pytest.mark.django_db
def test_votes_count_representation_two(
    mocker: MockerFixture, vote_form: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token
    Votes.objects.create(
        user=vote_form.admin,
        form=vote_form,
        vote=VoteFields.objects.all()[0],
    )
    Votes.objects.create(
        user=vote_form.admin,
        form=vote_form,
        vote=VoteFields.objects.all()[1],
    )

    serializer = VoteFormSerializer(
        instance=vote_form, context={"request": request_mock}
    )

    assert len(list(serializer.data["votes_count"])) == 2


@pytest.mark.django_db
def test_vote_fields_representation(
    mocker: MockerFixture, vote_form: VoteForm, user_token: User
):
    request_mock = mocker.Mock(spec=Request)
    request_mock.user = user_token

    serializer = VoteFormSerializer(
        instance=vote_form, context={"request": request_mock}
    )

    vote_fields = VoteFields.objects.filter(form=vote_form)
    vote_fields_serialized = VoteFieldsSerializer(
        instance=vote_fields, many=True
    )
    assert serializer.data["vote_fields"] == vote_fields_serialized.data
