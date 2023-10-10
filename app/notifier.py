from functools import partial
from typing import Any, Literal

from app.tasks import ms_email
from app.ms_manager import MSManager


def ms_notify(access_token: str, notification_payload: dict[str, Any]):
    ms_manager = MSManager(token=access_token)
    ms_manager.send_email(
        dict(
            subject=notification_payload['subject'],
            content=notification_payload['message'],
            content_type=notification_payload['content_type'],
            to_recipients=notification_payload['recipient_list'],
            attachments=notification_payload['files'],
            cc_recipients=None,
            save_to_sent_items=True,
        )
    )


def send_notification(
    notifier_type: Literal['email', 'outlook'],
    notification_payload: dict[str, Any],
    access_token: str
):
    notification_senders = {
        "email": ms_email.delay,
        "outlook": partial(ms_notify, access_token=access_token)
    }
    return notification_senders[notifier_type](notification_payload=notification_payload)
