from rest_framework.authentication import TokenAuthentication


# TODO: Add tests
class TokenAuthSupportCookie(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support cookie based authentication
    """

    def authenticate(self, request):
        # Check if "auth_token" is in the request cookies.
        if (
            "auth_token" in request.COOKIES
            and "HTTP_AUTHORIZATION" not in request.META
        ):
            return self.authenticate_credentials(
                request.COOKIES.get("auth_token")
            )
        return super().authenticate(request)
