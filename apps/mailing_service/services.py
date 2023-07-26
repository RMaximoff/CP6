import schedule
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from apps.mailing_service.models import Client, MailingLog, MailingSettings
from config import settings
from datetime import timedelta, datetime
import logging
from config.settings import CACHE_ENABLED

logging.basicConfig(level=logging.INFO)


def mailing_cache(owner_id):
    if CACHE_ENABLED:
        key = f'mailing_settings_list_{owner_id}'
        mailing_settings_list = cache.get(key)
        if mailing_settings_list is None:
            mailing_settings_list = MailingSettings.objects.filter(owner_id=owner_id)
            cache.set(key, mailing_settings_list)
    else:
        mailing_settings_list = MailingSettings.objects.filter(owner_id=owner_id)
    return mailing_settings_list


def send_mailing(mailing_id):
    """Отправка письма клиенту"""
    mailing = MailingSettings.objects.get(pk=mailing_id)
    current_time = timezone.now()

    if mailing.mailing_start_time <= current_time <= mailing.mailing_end_time:
        for client in mailing.clients.all():
            subject = mailing.mail.subject
            body = mailing.mail.body

            try:
                send_mail(subject, body, settings.EMAIL_HOST_USER, [client.email])
                MailingLog.objects.create(
                    mailing=mailing,
                    status='successful',
                    server_response='Сообщение успешно отправлено',
                )
            except Exception as e:
                MailingLog.objects.create(
                    mailing=mailing,
                    status='failed',
                    server_response=str(e),
                )





# def sending_mail(obj):
#     """Отправка письма клинту"""
#     status = []
#     clients = Client.objects.filter(pk=obj.clients.pk)
#     for client in clients:
#         try:
#             send_mail(
#                 obj.mail.subject,
#                 obj.mail.body,
#                 settings.EMAIL_HOST_USER,
#                 [client.email]
#             )
#         except Exception as e:
#             server_response = {
#                 'timestamp': datetime.now(),
#                 'status': 'failure',
#                 'server_response': f'Сообщение не отправлено. Ошибка:{str(e)}',
#                 'client': client.pk,
#             }
#             status.append(MailingLog(**server_response))
#             logging.error(f'Ошибка при отправке рассылки: {str(e)}')
#         else:
#             server_response = {
#                 'timestamp': datetime.now(),
#                 'status': 'success',
#                 'server_response': 'Сообщение успешно отправлено',
#                 'client': obj.clients,
#             }
#             status.append(MailingLog(**server_response))
#             logging.info('Рассылка успешно отправлена')
#     MailingLog.objects.bulk_create(status)
#
#
# def mailing():
#
#     mailings = MailingSettings.objects.all()
#     frequency = {'daily': 1, 'weekly': 7, 'monthly': 30}
#
#     for item in mailings:
#         if item.mailing_status == 'created' or item.mailing_status == 'started':
#             if item.mailing_start_time <= timezone.now() <= item.mailing_end_time \
#                     or item.mailing_start_time == timezone.now():
#                 item.mailing_status = 'started'
#                 item.mailing_start_time += timedelta(frequency.get(item.mailing_period))
#                 sending_mail(item)
#                 item.save()
#             elif item.mailing_end_time >= timezone.now():
#                 sending_mail(item)
#                 item.mailing_status = 'completed'
#                 item.save()
#
#
# def job():
#     schedule.every(60).seconds.do(mailing)
#     logging.info('Новая задача добавлена в планировщик')


