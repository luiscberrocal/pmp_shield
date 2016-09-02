from django.test import TestCase

from ...models import GradeLevel, PositionDescription, Position
from ..factories import GradeLevelFactory


class TestGradeLevel(TestCase):

    def test_initial_data(self):
        self.assertEqual(6, GradeLevel.objects.count())

    def test_create(self):
        grade = GradeLevelFactory.create(grade_type='NM', level=1)
        self.assertEqual('NM-01', str(grade))


class TestPositionDescription(TestCase):

    def test_initial_data(self):
        self.assertEqual(5, PositionDescription.objects.count())


class TestPosition(TestCase):

    def test_initial_data(self):
        self.assertEqual(19, Position.objects.count())
