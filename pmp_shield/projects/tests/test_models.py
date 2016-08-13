from django.test import TestCase

from ...risks.models import Risk
from ..models import Project, Assumption
from .factories import ProjectFactory


class TestProject(TestCase):

    def test_create(self):
        project = ProjectFactory.create()
        self.assertEqual(1, Project.objects.count())
        self.assertEqual(4, project.assumptions.count())
        self.assertEqual(4, project.risks.count())

    def test_create_batch(self):
        ProjectFactory.create_batch(5)
        self.assertEqual(5, Project.objects.count())
        self.assertEqual(20, Assumption.objects.count())
        self.assertEqual(20, Risk.objects.count())
