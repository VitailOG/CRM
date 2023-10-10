from typing import Any

from celery import shared_task

from django.core.mail import EmailMessage


@shared_task
def ms_email(notification_payload: dict[str, Any]):
    email = EmailMessage(
        notification_payload['subject'],
        notification_payload['message'],
        notification_payload['from_email'],
        notification_payload['recipient_list'],
    )
    email.content_subtype = notification_payload['content_type']
    for file_info in notification_payload['files']:
        email.attach(file_info['name'], file_info['content'], file_info['content_type'])
    email.send()

