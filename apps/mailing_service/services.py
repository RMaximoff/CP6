import schedule
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from apps.mailing_service.models import Client, MailingLog, MailingSettings
from config import settings
from datetime import timedelta, datetime
import logging


logging.basicConfig(level=logging.INFO)


def sending_mail(subject, body, clients_email):
    """Отправка письма"""
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        clients_email
    )


def send_mailing():
    """Рассылка"""
    mailings = MailingSettings.objects.all()
    current_time = timezone.now()
    frequency = {'daily': 1, 'weekly': 7, 'monthly': 30}

    for mailing in mailings:
        if mailing.mailing_status == 'created' or mailing.mailing_status == 'started':
            if mailing.mailing_start_time <= current_time <= mailing.mailing_end_time:
                for client in mailing.clients.all():
                    subject = mailing.mail.subject
                    body = mailing.mail.body
                    try:
                        send_mail(subject, body, settings.EMAIL_HOST_USER, [client.email])
                        MailingLog.objects.create(
                            mailing=mailing,
                            client=client,
                            status='successful',
                            server_response='Сообщение успешно отправлено',
                        )
                        mailing.mailing_status = 'started'
                        mailing.mailing_start_time += timedelta(days=frequency.get(mailing.mailing_period))
                        mailing.save()

                    except Exception as e:
                        MailingLog.objects.create(
                            mailing=mailing,
                            client=client,
                            status='failed',
                            server_response=str(e),
                        )
            elif mailing.mailing_end_time >= current_time:
                mailing.mailing_status = 'completed'
                mailing.save()
            else:
                pass


def job():
    schedule.every(60).seconds.do(send_mailing)
    logging.info('Новая задача добавлена в планировщик')


