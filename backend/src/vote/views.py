import json

from django.db.models import QuerySet
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vote.models import VoteForm
from vote.serializers import CreateVotesSerializer, VoteFormSerializer


class MakeVoteView(APIView):
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


# TODO: Add tests
class AdminVoteFormsListView(ListAPIView):
    serializer_class = VoteFormSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self) -> QuerySet[VoteForm]:
        user = self.request.user
        return VoteForm.objects.filter(admin=user).select_related("admin")  # type: ignore


# TODO: Add tests
class CreateVoteView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = CreateVotesSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
