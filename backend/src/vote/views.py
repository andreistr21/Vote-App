import json

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.generics import DestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vote.models import VoteForm, Votes
from vote.serializers import (
    CreateVotesSerializer,
    DeleteVotesSerializer,
    VoteFormSerializer,
)


class CreateVoteFormView(APIView):
    def post(self, request: Request) -> Response:
        form_data = {"admin": request.user.id} | request.data
        vote_form_serializer = VoteFormSerializer(data=form_data)
        if vote_form_serializer.is_valid() and vote_form_serializer.save():
            return Response(
                json.dumps({"details": "Form created successfully."}),
                status=status.HTTP_200_OK,
            )

        return Response(
            json.dumps({"errors": vote_form_serializer.errors}),
            status=status.HTTP_400_BAD_REQUEST,
        )


class AdminVoteFormsListView(ListAPIView):
    serializer_class = VoteFormSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self) -> QuerySet[VoteForm]:
        user = self.request.user
        return VoteForm.objects.filter(
            admin=user
        ).select_related(  # type: ignore
            "admin"
        )


class CreateVoteView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = CreateVotesSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# TODO: Add tests
class DeleteVoteView(DestroyAPIView):
    serializer_class = DeleteVotesSerializer

    def get_queryset(self) -> QuerySet[Votes]:
        return Votes.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            "user": self.request.user.id,
            "vote": self.request.data["vote"],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
