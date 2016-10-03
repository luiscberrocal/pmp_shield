from django.test import TestCase

from ....projects.tests.factories import BasicProjectFactory
from ...models import Goal
from ..factories import GoalFactory


class TestGoal(TestCase):

    def test_create(self):
        goal = GoalFactory.create(project=None, name='Cumplir con su horario de trabajo')
        self.assertEqual(1, Goal.objects.count())

    def test_create_with_project(self):
        project = BasicProjectFactory.create(name='Desarrollo de CTAN', description='Desarrollo de CTAN en .NET')
        goal = GoalFactory.create(project=project)
        self.assertEqual(1, Goal.objects.count())
        self.assertEqual(goal.name, project.name)
        self.assertEqual(goal.description, project.description)
