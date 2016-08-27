from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from ...models import Goal
from ....employees.models import OrganizationUnit
from ....projects.tests.factories import ProjectFactory


class TestCreateGoalsForProjects(TestCase):


    def test_create_goals_for_projects(self):
        content = StringIO()
        tino_ns = OrganizationUnit.objects.get(short_name='TINO-NS')
        ProjectFactory.create_batch(10, office=tino_ns)
        call_command('create_goals_for_projects', office='TINO-NS', stdout=content)
        results = self.get_results(content)

        self.assertEqual(10, Goal.objects.count())
        self.assertEqual(11, len(results))

    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results
