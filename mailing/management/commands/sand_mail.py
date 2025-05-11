import logging

from mailing.models import Mailing, MailingAttempt
from config.settings import DEFAULT_FROM_EMAIL
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.core.mail import send_mail
from datetime import timedelta, timezone


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Функция для отправки рассылок."""

    def handle(self, *args, **kwargs):
        time_threshold_start = timezone.now() - timedelta(hours=20)
        time_threshold_end = timezone.now()

        mailings = Mailing.objects.filter(
            Q(status=Mailing.CREATED) | Q(status=Mailing.RUNNING),
            first_send_at__gte=time_threshold_start,
            first_send_at__lte=time_threshold_end,
        )

        for mailing in mailings:
            mailing.status = Mailing.RUNNING
            mailing.save()

            recipients = mailing.recipients.all()
            for recipient in recipients:
                try:
                    logger.info(f"Отправка письма на {recipient.email}")
                    send_mail(
                        subject=mailing.message,
                        message=mailing.message.message,
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient.email],
                    )
                    status = MailingAttempt.SUCCESS
                    response = f"{recipient.email}: Успешно отправлено"
                    logger.info(response)

                except Exception as e:
                    status = MailingAttempt.FAILURE
                    response = f"{recipient.email}: Ошибка: {str(e)}"
                    logger.error(response)

                MailingAttempt.objects.create(
                    attempted_at=timezone.now(),
                    status=status,
                    mail_server_response=response,
                    mailing=mailing,
                )

            mailing.status = Mailing.COMPLETED
            mailing.save()
