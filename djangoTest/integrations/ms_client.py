from microsoftgraph.client import Client

from django.conf import settings

from djangoTest.integrations.ms_mail import Mail


client = Client(settings.CLIENT_ID, settings.SECRET_ID)
client.mail = Mail(client)
