from django.core.management import BaseCommand

from apps.users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Учетка админа
        user = User.objects.create(
            email='admin@admin.ru',
            is_staff=True,
            is_superuser=True,
            is_verified=True
        )

        user.set_password('111')
        user.save()

        # тестовые пользователи
        user = User.objects.create(
            email='test1@test.ru',
            is_verified=True
        )

        user.set_password('2222')
        user.save()

        user = User.objects.create(
            email='test2@test.ru',
            is_verified=True
        )

        user.set_password('3333')
        user.save()