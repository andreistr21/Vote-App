import json

import pytest
from django.contrib.auth.models import User
from pytest_mock import MockerFixture
from rest_framework.serializers import ModelSerializer, ValidationError

from vote.models import VoteForm
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


def test_validate_vote_fields():
    serializer = VoteFormSerializer()
    with pytest.raises(ValidationError):
        serializer.validate_vote_fields({})


def test_to_representation(mocker: MockerFixture):
    mocker.patch.object(ModelSerializer, "to_representation", return_value={"admin": 1})
    admin = User(id=1, username="test-username")
    vote_form = VoteForm(
        id=1,
        admin=admin,
        name="test-vote-form",
    )
    serializer = VoteFormSerializer()

    representation = serializer.to_representation(vote_form)

    assert representation == {"admin": "test-username"}
