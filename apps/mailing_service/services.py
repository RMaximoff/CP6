import schedule
from django.core.mail import send_mail
from django.utils import timezone
from apps.mailing_service.models import Client, MailingLog, MailingSettings
from config import settings
from datetime import timedelta, datetime
import csv


def read_client_csv(name):
    with open():
        pass


def sending_mail(obj):
    """Отправка письма клинту"""
    status = []
    clients = Client.objects.filter(pk=obj.clients.pk)
    for client in clients:
        try:
            send_mail(
                obj.mail.subject,
                obj.mail.body,
                settings.EMAIL_HOST_USER,
                [client.email]
            )
        except Exception as e:
            server_response = {
                'timestamp': datetime.now(),
                'status': 'failure',
                'server_response': f'Сообщение не отправлено. Ошибка:{str(e)}',
                'client': client.pk,
            }
            status.append(MailingLog(**server_response))
        else:
            server_response = {
                'timestamp': datetime.now(),
                'status': 'success',
                'server_response': 'Сообщение успешно отправлено',
                'client': obj.clients,
            }
            status.append(MailingLog(**server_response))
    MailingLog.objects.bulk_create(status)


def mailing():
    print("гружу модель")
    mailings = MailingSettings.objects.all()
    frequency = {'daily': 1, 'weekly': 7, 'monthly': 30}
    print("загрузил")
    for item in mailings:
        print("проход цикла")
        if item.mailing_status == 'paused':
            pass
        else:
            if item.mailing_status == 'created' or item.mailing_status == 'started':
                if item.mailing_start_time <= timezone.now() <= item.mailing_end_time \
                        or item.mailing_start_time == timezone.now():
                    item.mailing_status = 'running'
                    item.mailing_start_time += timedelta(frequency.get(item.mailing_period))
                    print("отправляю письмо")
                    sending_mail(item)
                    item.save()
                elif item.end_time >= timezone.now():
                    print("отправляю письмо")
                    sending_mail(item)
                    item.mailing_status = 'completed'
                    item.save()


def job():
    schedule.every(60).seconds.do(mailing)
