import requests

from django.conf import settings

from djangoTest.integrations.ms_client import client


def set_token(method):
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            # set token
            self.exchange_code()
        client.set_token({"access_token": self.token})
        return method(self, *args, **kwargs)
    return wrapper


class MSManager:

    def __init__(self, *, code: str | None = None, token: str | None = None):
        self.code = code
        self.token = token

    def exchange_code(self):
        response = client.exchange_code(settings.REDIRECT_URI, self.code)
        self.token = response.data['access_token']
        return response.data

    def refresh(self, refresh_token: str):
        response = client.refresh_token(settings.REDIRECT_URI, refresh_token)
        return response.data

    @set_token
    def get_user(self):
        response = client.users.get_me()
        return response.data

    @set_token
    def get_messages(self, client_email: str):
        url = f'https://graph.microsoft.com/v1.0/users/{client_email}/messages'
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get(url, headers=headers)
        return response.json()

    @set_token
    def send_email(self, data: dict):
        client.mail.send_mail(**data)
