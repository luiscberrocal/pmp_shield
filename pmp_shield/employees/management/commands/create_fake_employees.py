import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ...tests.factories import EmployeeFactory
from ...models import Employee

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage
        $ python manage.py create_employee -u oaherrera jduarte
    """

    def add_arguments(self, parser):
        #parser.add_argument('output_filename')
        parser.add_argument("-c", "--count",
                            dest="employee_count",
                            help="Create fake employess",
                            )

    def handle(self, *args, **options):
        count = int(options['employee_count'])
        employees = EmployeeFactory.create_batch(count)
        for employee in employees:
            self.stdout.write('Created employee %s' % (employee))

