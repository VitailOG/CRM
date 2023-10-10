from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from app.models import UserToken


class MicrosoftAccessTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        access_token = self.validate_token(request.META.get('HTTP_AUTHORIZATION', None))

        user_token = (
            UserToken.objects
            .filter(access_token=access_token)
            .order_by('-created_at')
            .first()
        )

        if user_token is None:
            raise AuthenticationFailed("Must be auth4")

        if "refresh" not in request.path_info and user_token.is_valid():
            raise AuthenticationFailed("Must be auth5")

        setattr(request, "access_token", access_token)

        return user_token.user, None

    def validate_token(self, authorization_header: str | None):
        if authorization_header is None:
            raise AuthenticationFailed("Must be auth1")

        auth_split = authorization_header.split()

        if len(auth_split) != 2:
            raise AuthenticationFailed("Must be auth2")

        keyword, token = auth_split

        if self.keyword != keyword:
            raise AuthenticationFailed("Must be auth3")

        return token


class MSAuthView(APIView):
    authentication_classes = [MicrosoftAccessTokenAuthentication]
