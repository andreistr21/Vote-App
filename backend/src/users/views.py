import json

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "You are already logged in."},
                status=status.HTTP_200_OK,
            )

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user_serializer = UserSerializer(user)
                data = {
                    "detail": "Login successful.",
                    "user": user_serializer.data,
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
