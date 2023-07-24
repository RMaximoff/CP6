import json
from django.core.management import BaseCommand

from django.db import connection
from apps.users.models import User
from apps.blog.models import Blog
from apps.mailing_service.models import Client, MailingSettings, MailingMessage, MailingLog


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Client.objects.all().delete()
        MailingSettings.objects.all().delete()
        MailingMessage.objects.all().delete()
        MailingLog.objects.all().delete()
        Blog.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_version_id_seq RESTART WITH 1;")

        with open('client.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            data_for_create = []
            for item in data:
                data_fields = item['fields']
                data_instance = Client(**data_fields)
                data_for_create.append(data_instance)
            Client.objects.bulk_create(data_for_create)

        with open('product.json', 'r', encoding='utf-8') as file:
            products = json.load(file)
            products_for_create = []
            for product_data in products:
                product_fields = product_data['fields']
                product_fields['category'] = Category.objects.get(pk=product_fields['category'])
                user_id = product_fields.pop('user')  # Получаем и удаляем идентификатор пользователя
                user = User.objects.get(id=user_id)  # Получаем экземпляр пользователя по идентификатору
                product_fields['user'] = user
                product_instance = Product(**product_fields)
                products_for_create.append(product_instance)
            Product.objects.bulk_create(products_for_create)

        with open('version.json', 'r', encoding='utf-8') as file:
            versions = json.load(file)

            versions_for_create = []
            for version_data in versions:
                version_fields = version_data['fields']
                version_fields['product'] = Product.objects.get(pk=version_fields['product'])
                version_instance = Version(**version_fields)
                versions_for_create.append(version_instance)
            Version.objects.bulk_create(versions_for_create)

