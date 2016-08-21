import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ...tests.factories import EmployeeFactory
from ...models import Employee, OrganizationUnit

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage
        $ python manage.py create_fake_employees -c 10 --unit=TINO-NS
    """

    def add_arguments(self, parser):
        #parser.add_argument('output_filename')
        parser.add_argument("-c", "--count",
                            dest="employee_count",
                            help="Create fake employess",
                            )
        parser.add_argument("--office",
                            dest="office",
                            help="Organizational unit",
                            default=None,
                            )

    def handle(self, *args, **options):
        office = None
        if options['office'] != None:
            office = OrganizationUnit.objects.get(short_name=options['unit'])

        count = int(options['employee_count'])
        if office:
            employees = EmployeeFactory.create_batch(count, office=office)
        else:
            employees = EmployeeFactory.create_batch(count)

        for employee in employees:
            self.stdout.write('Created employee %s' % (employee))

