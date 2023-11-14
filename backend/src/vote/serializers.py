import json

from django.db import IntegrityError
from rest_framework import serializers

from vote.models import VoteFields, VoteForm, Votes


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = "__all__"


class VoteFieldsSerializer(serializers.ModelSerializer):
    votes = VotesSerializer(many=True, read_only=True)

    class Meta:
        model = VoteFields
        fields = "__all__"


class VoteFormSerializer(serializers.ModelSerializer):
    vote_fields = VoteFieldsSerializer(many=True)
    votes = VotesSerializer(many=True, read_only=True)

    class Meta:
        model = VoteForm
        fields = "__all__"

    def create(self, validated_data) -> VoteForm:
        vote_fields_data = validated_data.pop("vote_fields")
        # TODO: Check if vote fields contains at least (1\2?) fields
        try:
            vote_form = VoteForm.objects.create(**validated_data)
        except IntegrityError as integrity_error:
            error_msg = str(integrity_error)
            if "closing_greater_than_created" in error_msg:
                raise serializers.ValidationError(
                    self._get_closing_greater_than_created_error_data()
                ) from integrity_error

            raise serializers.ValidationError(
                self._get_unknown_error_data(error_msg)
            ) from integrity_error

        vote_fields_to_create = [
            VoteFields(form=vote_form, **data) for data in vote_fields_data
        ]
        VoteFields.objects.bulk_create(vote_fields_to_create)

        return vote_form

    def _get_closing_greater_than_created_error_data(self) -> str:
        return json.dumps(
            {
                "errors": {
                    "Form closing date": (
                        "Closing date should be greater then creation"
                    )
                }
            }
        )

    def _get_unknown_error_data(self, error_msg: str) -> str:
        return json.dumps({"errors": {"Unknown error": (error_msg)}})
