from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model

from app.models import UserToken


User = get_user_model()


class DBManager:

    def create_user(self, user_data: dict[str, str]):
        user, _ = User.objects.update_or_create(
            username=user_data['userPrincipalName'],
            defaults={
                'first_name': user_data['givenName'],
                'last_name': user_data['surname'],
                'email': user_data['mail'],
            }
        )
        return user

    def create_token(self, data: dict):
        UserToken.objects.create(
            user_id=data['user_id'],
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expiration_date=timezone.now() + timedelta(seconds=data['expires_in'])
        )
