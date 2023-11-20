import json

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vote.models import VoteForm
from vote.serializers import VoteFormSerializer


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


class AdminVoteFormsListView(ListAPIView):
    serializer_class = VoteFormSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        user = self.request.user
        return VoteForm.objects.filter(admin=user)  # type: ignore
