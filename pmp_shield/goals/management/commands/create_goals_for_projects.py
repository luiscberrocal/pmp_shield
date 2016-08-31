import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ....projects.models import Project, ProjectMembership
from ...models import Employee, Goal, EmployeeGoal, ExpectationsList

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage
        $ python manage.py create_goals_for_projects --office=TINO-NS
    """

    def add_arguments(self, parser):
        parser.add_argument("--office",
                            dest="office",
                            help="Office short name",
                            )

        parser.add_argument("--fiscal-year",
                            dest="fiscal_year",
                            help="Fical Year",
                            )


    def handle(self, *args, **options):
        projects = Project.objects.filter(office__short_name=options['office'], fiscal_year=options['fiscal_year'])
        count = 0
        count_created = 0
        for project in projects:
            start_date, end_date = project.start_end_dates()
            expectations = 'Haber alcanzado el %d%% de avance antes del %s.' \
                                    % (90,  end_date.strftime('%d-%b-%Y'))
            goal, created = Goal.objects.get_or_create(project=project, expectations=expectations)
            self.stdout.write('Goal: %s created: %s' % (goal, created))
            for member in project.members.all():
                employee_expectations = expectations
                if member.role == ProjectMembership.LEADER_ROLE:
                    employee_expectations +=' Apoyar al supervisor en la gestión administrativa.'
                expectations_list, _ = ExpectationsList.objects.get_or_create(version=1, employee=member.member,
                                                                           fiscal_year='AF16')

                employee_goal, _ = EmployeeGoal.objects.get_or_create(employee=member.member, goal=goal,
                                                            expectations=employee_expectations, weight= 0.1,
                                                            expectations_list=expectations_list)
            count += 1
            if created:
                count_created += 1
        self.stdout.write('Created %d goals for %s' % (count_created, options['office']))
