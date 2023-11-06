import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.selectors import get_or_create_token_by_user, get_token_by_key
from users.serializers import UserLoginSerializer, UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        if token := self._is_user_already_logged_in(request):
            return self._get_already_logged_in_response(token)

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return self._get_successful_login_response(serializer)

        return self._get_invalid_credentials_response()

    def _is_user_already_logged_in(self, request: Request) -> Token | None:
        if authorization_token := request.META.get("HTTP_COOKIE"):
            token_key = authorization_token.split(" ")[1]
            return get_token_by_key(token_key) or None
        return None

    def _get_already_logged_in_response(self, token: Token) -> Response:
        user = Token.objects.get(key=token.key).user
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
        user = serializer.validated_data["user"]
        token = get_or_create_token_by_user(user)
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
