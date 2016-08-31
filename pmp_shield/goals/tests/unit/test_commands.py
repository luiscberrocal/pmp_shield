from io import StringIO

from datetime import date
from django.core.management import call_command
from django.test import TestCase

from ...models import Goal
from ....employees.models import OrganizationUnit
from ....projects.tests.factories import ProjectFactory


class TestCreateGoalsForProjects(TestCase):


    def test_create_goals_for_projects(self):
        content = StringIO()
        tino_ns = OrganizationUnit.objects.get(short_name='TINO-NS')
        ProjectFactory.create_batch(10, office=tino_ns, milestones={'start_date': date(2015, 10,1)})
        ProjectFactory.create_batch(10, office=tino_ns, milestones={'start_date': date(2014, 10, 1)})
        call_command('create_goals_for_projects', office='TINO-NS', fiscal_year='AF16', stdout=content)
        results = self.get_results(content)

        self.assertEqual(10, Goal.objects.count())
        self.assertEqual(11, len(results))
        self.assertEqual('Created 10 goals for TINO-NS', results[10])

    def test_create_goals_for_projects_not_created(self):
        content = StringIO()
        tino_ns = OrganizationUnit.objects.get(short_name='TINO-NS')
        ProjectFactory.create_batch(5, office=tino_ns, milestones={'start_date': date(2015, 10, 1)})
        call_command('create_goals_for_projects', office='TINO-NS', fiscal_year='AF16')
        call_command('create_goals_for_projects', office='TINO-NS', fiscal_year='AF16', stdout=content)
        results = self.get_results(content)

        self.assertEqual(5, Goal.objects.count())
        self.assertEqual(6, len(results))
        self.assertEqual('Created 0 goals for TINO-NS', results[5])

    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results
