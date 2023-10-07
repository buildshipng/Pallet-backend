import logging
import secrets
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import TemplateDoesNotExist, render_to_string

from account.utils import abort



Logger = logging.getLogger()

def generate_token():
    """
    Generates 6 digit random token for user 
    email verification and password reset view
    """
    otp = "".join([f"{secrets.randbelow(10)}" for _ in range(6)])
    return otp


class EmailManagerError(Exception):
    """Raise an exception if an error occurs in the email manager"""


class EmailManager:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def send_mail(
        self,
        subject: str,
        recipients: list[str],
        context: dict[str, Any] or None,
        template_name: str or None,
        message: str or None = None,
        ) -> None:
        try:
            """Send email to valid email address."""
            if (context and template_name is None) or (template_name and context is None):
                raise EmailManagerError(
                    "context set but template_name not set Or template_name set and context not set."
                )
            if (context is None) and (template_name is None) and (message is None):
                raise EmailManagerError(
                    "Must set either {context and template_name} or message args."
                )
                
            html_message: str | None = None
            
            if context is not None:
                # Html message
                # try:
                #     html_message = render_to_string(
                #         template_name=template_name, context=context
                #     )

                # except TemplateDoesNotExist as error:
                #     print("heri")

                #     raise EmailManagerError(str(error))
                html_message = render_to_string(
                        template_name=template_name, context=context
                    )
                
                try:
                    send_mail(
                        from_email=settings.EMAIL_HOST_USER,
                        subject=subject,
                        recipient_list=recipients,
                        fail_silently=False,
                        message=message,
                        html_message=html_message
                    )

                except Exception as error:
                    print("sent")
                    
                    Logger.log(msg=error, level=logging.ERROR)
        except EmailManagerError as e:
            abort(401, str(e))