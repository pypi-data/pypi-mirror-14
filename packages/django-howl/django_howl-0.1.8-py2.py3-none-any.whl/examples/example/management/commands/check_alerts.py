import logging

from django.core.management.base import BaseCommand

from example.models import DataPooling


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.debug('>>  Checking alerts...')

        for data in DataPooling.objects.all():
            data.observer.compare(data.last_measurement)

        logger.debug('>>  All alerts checked!')
