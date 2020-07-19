from __future__ import absolute_import, unicode_literals
import os
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from config.settings import development
FROM_EMAIL = development.EMAIL_HOST_USER

@shared_task
def simple_mail(subject, message, from_email, recipient_list,
                fail_silently=False, auth_user=None, auth_password=None,
                connection=None, html_message=None):
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
            auth_user=auth_user,
            auth_password=auth_password,
            connection=connection,
            html_message=html_message,
            )
