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

    def create(self, validated_data):
        vote_fields_data = validated_data.pop("vote_fields")
        vote_form = VoteForm.objects.create(**validated_data)

        vote_fields_to_create = [
            VoteFields(form=vote_form, **data) for data in vote_fields_data
        ]
        VoteFields.objects.bulk_create(vote_fields_to_create)

        return vote_form
