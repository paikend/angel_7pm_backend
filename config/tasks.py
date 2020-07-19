import os
from django.core.mail import send_mail
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from django.core.mail import EmailMultiAlternatives
from collections import defaultdict
@shared_task
def simple_mail(subject, message, from_email, recipient_list,
                fail_silently=False, auth_user=None, auth_password=None,
                connection=None, html_message=None):

    if ('DJANGO_SETTINGS_MODULE' in os.environ) and (
        os.environ['DJANGO_SETTINGS_MODULE'] == 'pearl.settings.development'):

        logger.info("Sent email")
        print("The time is %s :" % str(datetime.now()))

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

    elif ('DJANGO_SETTINGS_MODULE' in os.environ) and (
        os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.production'):

        logger.info("Sent email")
        print("The time is %s :" % str(datetime.now()))

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

@shared_task
def test():
    print("hello")
