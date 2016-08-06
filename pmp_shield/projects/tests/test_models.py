from django.test import TestCase

from ..models import Project
from .factories import ProjectFactory


class TestProject(TestCase):

    def test_create(self):
        project = ProjectFactory.create()
        self.assertEqual(1, Project.objects.count())
        self.assertEqual(4, project.assumptions.count())
