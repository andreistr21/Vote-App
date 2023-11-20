import json
from datetime import timedelta
from typing import Any

import pytest
from django.db import IntegrityError
from django.utils import timezone
from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from vote.models import VoteFields, VoteForm
from vote.serializers import VoteFormSerializer


def test__get_unknown_error_data():
    error_msg = "Test error message"
    serializer = VoteFormSerializer()

    result = serializer._get_unknown_error_data(error_msg)

    assert result == json.dumps({"errors": {"Unknown error": (error_msg)}})


def test__get_closing_greater_than_created_error_data():
    serializer = VoteFormSerializer()

    result = serializer._get_closing_greater_than_created_error_data()

    assert result == json.dumps(
        {
            "errors": {
                "Form closing date": (
                    "Closing date should be greater then creation"
                )
            }
        }
    )


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
