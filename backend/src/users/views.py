import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        if request.auth:
            return self._get_already_logged_in_response(
                request.user  # type: ignore
            )

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return self._get_successful_login_response(serializer)

        return self._get_invalid_credentials_response()

    def _get_already_logged_in_response(self, user: User) -> Response:
        user_serializer = UserSerializer(user)

        return Response(
            json.dumps(
                {
                    "detail": "You are already logged in.",
                    "user": user_serializer.data,
                }
            ),
            status=status.HTTP_200_OK,
        )

    def _get_successful_login_response(
        self, serializer: UserLoginSerializer
    ) -> Response:
        user: User = serializer.validated_data["user"]
        token = user.auth_token
        user_serializer = UserSerializer(user)
        data = {
            "detail": "Login successful.",
            "user": user_serializer.data,
            "token": token.key,
        }
        return Response(
            json.dumps(data),
            content_type="JSON",
            status=status.HTTP_200_OK,
        )

    def _get_invalid_credentials_response(self) -> Response:
        return Response(
            json.dumps({"error": "Invalid credentials"}),
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        
class GetUsernameView(APIView):
    def get(self, request:Request) -> Response:
        data = json.dumps({"username": request.user.username})
        return Response(data)
