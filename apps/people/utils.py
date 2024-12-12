import logging

logger = logging.getLogger(__name__)
import requests
from decouple import config
from post_office import mail


def send_notification(recipient, context=None):
        template = context["template"]
        mail.send(
            recipient,
            config("DEFAULT_FROM_EMAIL"),
            template=template,
            context=context["context"],
            priority="now",
        )


def send_login_credentials(email,password):
        context = {
            "template": "login-credentials",
            "context": {
                "email": email,
                "password":password,
            }
        }

        send_notification(email, context=context)


