from acp_calendar.models import FiscalYear
from django.core.management import BaseCommand
from django.conf import settings
import logging
from datetime import datetime
from ...tests.factories import EmployeeFactory
from ...models import Employee, OrganizationUnit, UnitAssignment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    """

    def add_arguments(self, parser):
        #parser.add_argument('output_filename')
        parser.add_argument("-l", "--list",
                            action='store_true',
                            dest="list",
                            help="List employees",
                            )
        parser.add_argument("--office",
                            dest="office",
                            help="Organizational unit short name",
                            default=None,
                            )
        parser.add_argument("--fiscal-year",
                            dest="fiscal_year",
                            help="Fiscal year for assignments",
                            default=None,
                            )

    def handle(self, *args, **options):
        office = None
        office_title = 'All'

        if options['office'] != None:
            office = OrganizationUnit.objects.get(short_name=options['office'])
            office_title = options['office']

        if options['fiscal_year'] != None:
            fiscal_year = int(options['fiscal_year'])
        else:
            fy = FiscalYear.create_from_date(datetime.now())
            fiscal_year = fy.year

        if office:
            assignments = UnitAssignment.objects.get_fiscal_year_assignments_to(fiscal_year, office).order_by('employee__last_name')
        self.stdout.write('Office: %s FY: %d' % (office_title, fiscal_year))
        self.stdout.write('-'*100)
        num = 1
        for assignment in assignments:
            self.stdout.write('%2d. %-30s %-10s %-10s %4d' % (num, assignment.employee,
                                                 assignment.start_date, assignment.end_date,
                                                 assignment.age))
            num += 1

