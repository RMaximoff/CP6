from django.db import models


class Client(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email


class MailingSettings(models.Model):
    MAILING_PERIOD_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    mailing_time = models.TimeField()
    mailing_period = models.CharField(max_length=10, choices=MAILING_PERIOD_CHOICES)
    mailing_status = models.CharField(max_length=10, default='created')

    def __str__(self):
        return f"{self.get_mailing_period_display()} рассылка в {self.mailing_time}"


class MailingMessage(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class MailingLog(models.Model):
    MAILING_STATUS_CHOICES = (
        ('attempted', 'Попытка отправки'),
        ('successful', 'Успешно отправлено'),
        ('failed', 'Не удалось отправить'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=MAILING_STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_status_display()} ({self.timestamp})"
