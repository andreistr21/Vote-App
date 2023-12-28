import json

from django.db import IntegrityError
from django.db.models import Count, QuerySet
from django.utils import timezone
from rest_framework import serializers

from vote.models import VoteFields, VoteForm, Votes


class CreateVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fixes "object has no attribute 'initial_data'" and "This QueryDict
        # instance is immutable" errors in browsable API
        if hasattr(self, "initial_data") and not self.initial_data.get("user"):
            self.initial_data["user"] = self.context["request"].user.id

    def validate_vote(self, data: VoteFields) -> VoteFields:
        if data.form.votes_type == 1:
            self.only_one_vote_per_user_validation(data)
        elif data.form.votes_type == 2:
            self.only_one_vote_per_field_per_user(data)

        return data

    def only_one_vote_per_user_validation(self, data: VoteFields) -> None:
        if Votes.objects.filter(
            user=self.context["request"].user.id, form=data.form.id
        ):
            raise serializers.ValidationError(
                {
                    "errors": {
                        "vote": (
                            "User already voted for this form. Delete"
                            " previous vote if you want to change it."
                        )
                    }
                }
            )

    def only_one_vote_per_field_per_user(self, data: VoteFields) -> None:
        if Votes.objects.filter(
            user=self.context["request"].user.id, vote=data.id
        ):
            raise serializers.ValidationError(
                {
                    "errors": {
                        "vote": (
                            "User already voted for this field. Delete"
                            " previous vote if you want to change it."
                        )
                    }
                }
            )


class DeleteVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = "__all__"


class VoteFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteFields
        fields = "__all__"


class VoteFormSerializer(serializers.ModelSerializer):
    vote_fields = VoteFieldsSerializer(many=True)
    votes_count = serializers.SerializerMethodField()
    user_vote_id = serializers.SerializerMethodField()

    class Meta:
        model = VoteForm
        fields = "__all__"

    def to_representation(self, instance: VoteForm):
        representation = super().to_representation(instance)
        representation["admin"] = instance.admin.username
        return representation

    def get_votes_count(self, vote_form: VoteForm) -> QuerySet | list:
        if (
            vote_form.statistics_type == 2
            and timezone.now() < vote_form.closing
        ):
            return []
        return (
            Votes.objects.filter(form=vote_form)
            .values("vote")
            .annotate(vote_count=Count("id"))
        )

    def get_user_vote_id(self, vote_form: VoteForm):
        return Votes.objects.filter(
            user=self.context["request"].user, form=vote_form
        ).values_list("vote", flat=True)

    def validate_vote_fields(self, data: dict) -> dict:
        # Validates if at least two fields received
        if len(data) < 2:
            raise serializers.ValidationError(
                json.dumps(
                    {
                        "errors": {
                            "Vote fields": (
                                "Number of fields should be at least 2"
                            )
                        }
                    }
                )
            )
        return data

    def create(self, validated_data: dict) -> VoteForm:
        vote_fields_data = validated_data.pop("vote_fields")
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
