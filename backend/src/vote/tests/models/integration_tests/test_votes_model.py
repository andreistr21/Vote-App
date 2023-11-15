import pytest
from django.contrib.auth.models import User

from vote.models import VoteFields, VoteForm, Votes


@pytest.fixture
def create_vote_field(vote_form: VoteForm) -> tuple[VoteForm, VoteFields]:
    vote_field = VoteFields.objects.create(
        form=vote_form,
        name="test-field-name",
    )

    return vote_form, vote_field


@pytest.mark.django_db
class TestDunderMethods:
    def test_str(
        self, create_vote_field: tuple[VoteForm, VoteFields], user: User
    ):
        vote_form, vote_field = create_vote_field
        vote = Votes.objects.create(user=user, form=vote_form, vote=vote_field)

        assert str(vote) == f"Vote: {vote_field}"
