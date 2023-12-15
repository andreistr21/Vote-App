import pytest
from pytest_mock import MockerFixture
from pytest_mock.plugin import MockType
from rest_framework import serializers

from vote.serializers import CreateVotesSerializer


@pytest.fixture
def mocked_parent_init(mocker: MockerFixture) -> MockType:
    return mocker.patch.object(serializers.ModelSerializer, "__init__")


@pytest.fixture
def create_votes_serializer(
    mocked_parent_init: MockType,
) -> CreateVotesSerializer:
    return CreateVotesSerializer()


class TestInit:
    def test_parent_init_called(self, mocked_parent_init: MockType) -> None:
        CreateVotesSerializer()

        mocked_parent_init.assert_called_once_with()

    def test_set_user_id(
        self,
        mocker: MockerFixture,
    ) -> None:
        """
        Test case, when serializer has initial_data attr but not user object.
        """
        request = mocker.Mock()
        request.user.id = 11
        context = {"request": request}

        create_votes_serializer = CreateVotesSerializer(
            data={}, context=context
        )

        assert create_votes_serializer.initial_data["user"] == 11


class TestValidateVote:
    @pytest.fixture
    def mocks_for_validate_vote(self, mocker: MockerFixture) -> list[MockType]:
        """
        Returns list with this values by index(same as appearance in the code):
            0 - only_one_vote_per_user_validation
            1 - only_one_vote_per_field_per_user
        """
        return [
            mocker.patch.object(
                CreateVotesSerializer, "only_one_vote_per_user_validation"
            ),
            mocker.patch.object(
                CreateVotesSerializer, "only_one_vote_per_field_per_user"
            ),
        ]

    def test_validate_vote_single_choice(
        self,
        mocker: MockerFixture,
        mocks_for_validate_vote: list[MockType],
    ) -> None:
        vote_fields = mocker.Mock()
        vote_fields.form.votes_type = 1
        create_votes_serializer = CreateVotesSerializer()

        output = create_votes_serializer.validate_vote(vote_fields)

        mocks_for_validate_vote[0].assert_called_once_with(vote_fields)
        mocks_for_validate_vote[1].assert_not_called()
        assert output == vote_fields

    def test_validate_vote_multiple_choice(
        self,
        mocker: MockerFixture,
        mocks_for_validate_vote: list[MockType],
    ) -> None:
        vote_fields = mocker.Mock()
        vote_fields.form.votes_type = 2
        create_votes_serializer = CreateVotesSerializer()

        output = create_votes_serializer.validate_vote(vote_fields)

        mocks_for_validate_vote[0].assert_not_called()
        mocks_for_validate_vote[1].assert_called_once_with(vote_fields)
        assert output == vote_fields
