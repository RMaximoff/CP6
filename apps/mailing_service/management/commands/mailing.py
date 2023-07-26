import time
import schedule
from django.core.management import BaseCommand


from apps.mailing_service.services import job


class Command(BaseCommand):
    def handle(self, *args, **options):
        job()
        while True:
            schedule.run_pending()
            time.sleep(1)
