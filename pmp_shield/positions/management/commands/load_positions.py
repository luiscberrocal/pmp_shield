import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ...excel import import_positions_from_excel


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    """

    def add_arguments(self, parser):
        parser.add_argument('output_filename')


    def handle(self, *args, **options):
        filename = options['output_filename']
        res = import_positions_from_excel(filename)
        self.stdout.write('Added %d positions' % res)
