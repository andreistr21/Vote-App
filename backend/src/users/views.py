import json

from django.contrib.auth import login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if authorization_header := request.META.get("HTTP_COOKIE"):
            token = authorization_header.split(" ")[1]
            if Token.objects.filter(key=token).first():
                return Response(
                    {"detail": "You are already logged in."},
                    status=status.HTTP_200_OK,
                )

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
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

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )
