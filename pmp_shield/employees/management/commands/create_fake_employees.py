import os

from django.core.management import BaseCommand
from django.conf import settings
import logging
from datetime import datetime
from ...tests.factories import EmployeeFactory
from ...models import Employee, OrganizationUnit

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    To create 10 employees from any office:

        $ python manage.py create_fake_employees -c 10

    To create 10 employees for a specfic office:

        $ python manage.py create_fake_employees -c 10 --office=TINO-NS

    To create 10 employees for a specfic office with assignments startign at oct 1, 2016:

        $ python manage.py create_fake_employees -c 10 --office=TINO-NS --assignment-date=2016-10-1
    """

    def add_arguments(self, parser):
        #parser.add_argument('output_filename')
        parser.add_argument("-c", "--count",
                            dest="employee_count",
                            help="Create fake employess",
                            )
        parser.add_argument("--office",
                            dest="office",
                            help="Organizational unit short name",
                            default=None,
                            )
        parser.add_argument("--assignment-date",
                            dest="assignment_date",
                            help="Date when the assignment starts",
                            default=None,
                            )

    def handle(self, *args, **options):
        office = None
        assignment_date = None

        if options['office'] != None:
            office = OrganizationUnit.objects.get(short_name=options['office'])

        if options['assignment_date'] != None:
            assignment_date = datetime.strptime(options['assignment_date'], '%Y-%m-%d').date()

        count = int(options['employee_count'])
        if office:
            employees = EmployeeFactory.create_batch(count, office=office)
            if assignment_date:
                for employee in employees:
                    employee.assign_to_office(office, assignment_date)
        else:
            employees = EmployeeFactory.create_batch(count)

        for employee in employees:
            self.stdout.write('Created employee %s' % (employee))

