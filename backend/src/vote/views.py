import json

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vote.serializers import VoteFormSerializer


class MakeVoteView(APIView):
    def post(self, request: Request) -> Response:
        vote_form_serializer = VoteFormSerializer(data=request.data)
        if vote_form_serializer.is_valid():
            vote_form_serializer.save()
            return Response(
                json.dumps({"details": "Form created successfully."}),
                status=status.HTTP_200_OK,
            )

        return Response(json.dumps({"errors": vote_form_serializer.errors}))
