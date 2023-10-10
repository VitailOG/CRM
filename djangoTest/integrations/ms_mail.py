import base64

from microsoftgraph.response import Response
from microsoftgraph.mail import Mail as BaseMail
from microsoftgraph.decorators import token_required


class Mail(BaseMail):
    @token_required
    def send_mail(
            self,
            subject: str,
            content: str,
            to_recipients: list,
            cc_recipients: list = None,
            content_type: str = "HTML",
            attachments: list = None,
            save_to_sent_items: bool = True,
            **kwargs,
    ) -> Response:
        # Create recipient list in required format.
        if isinstance(to_recipients, list):
            if all([isinstance(e, str) for e in to_recipients]):
                to_recipients = [{"EmailAddress": {"Address": address}} for address in to_recipients]
        elif isinstance(to_recipients, str):
            to_recipients = [{"EmailAddress": {"Address": to_recipients}}]
        else:
            raise Exception("to_recipients value is invalid.")

        if cc_recipients and isinstance(cc_recipients, list):
            if all([isinstance(e, str) for e in cc_recipients]):
                cc_recipients = [{"EmailAddress": {"Address": address}} for address in cc_recipients]
        elif cc_recipients and isinstance(cc_recipients, str):
            cc_recipients = [{"EmailAddress": {"Address": cc_recipients}}]
        else:
            cc_recipients = []

        # Create list of attachments in required format.
        attached_files = []
        if attachments:
            for attachment in attachments:
                b64_content = base64.b64encode(attachment.read())
                attached_files.append(
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "ContentBytes": b64_content.decode("utf-8"),
                        "ContentType": attachment.content_type,
                        "Name": attachment.name,
                    }
                )

        # Create email message in required format.
        email_msg = {
            "Message": {
                "Subject": subject,
                "Body": {"ContentType": content_type, "Content": content},
                "ToRecipients": to_recipients,
                "ccRecipients": cc_recipients,
                "Attachments": attached_files,
            },
            "SaveToSentItems": save_to_sent_items,
        }
        email_msg.update(kwargs)

        # Do a POST to Graph's sendMail API and return the response.
        return self._client._post(self._client.base_url + "me/sendMail", json=email_msg)
