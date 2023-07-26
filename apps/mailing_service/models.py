from django.db import models
from apps.users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=255, verbose_name="Имя клиента")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена')
    )

    title = models.CharField(max_length=50, verbose_name='Название')
    mailing_start_time = models.DateTimeField(**NULLABLE, verbose_name='Дата рассылки')
    mailing_end_time = models.DateTimeField(**NULLABLE, verbose_name='Финиш рассылки')
    mailing_period = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Периодичность рассылки')
    mailing_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    mail = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.get_mailing_period_display()} рассылка в {self.mailing_start_time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    MAILING_STATUS = (
        ('successful', 'Успешно отправлено'),
        ('failed', 'Не удалось отправить'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=MAILING_STATUS)
    server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Client, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"{self.get_status_display()} ({self.timestamp})"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('-timestamp',)

