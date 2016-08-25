import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ....projects.models import Project
from ...models import Employee, Goal

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


    def handle(self, *args, **options):
        projects = Project.objects.filter(office__short_name=options['office'])
        count = 0
        count_created = 0
        for project in projects:
            start_date, end_date = project.start_end_dates()
            expectations = 'Haber alcanzado el %d%% de avance antes del %s.' \
                                    % (90,  end_date.strftime('%d-%b-%Y'))
            goal, created = Goal.objects.get_or_create(project=project, expectations=expectations)
            self.stdout.write('Goal: %s created: %s' % (goal, created))
            count += 1
            if created:
                count_created += 1
        self.stdout.write('Created %d goals for %s' % (count_created, options['office']))
