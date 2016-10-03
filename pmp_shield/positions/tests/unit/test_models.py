from datetime import date
from django.test import TestCase

from pmp_shield.employees.models import OrganizationUnit
from pmp_shield.employees.tests.factories import EmployeeFactory
from ...models import GradeLevel, PositionDescription, Position, PositionEmployeeAssignment
from ..factories import GradeLevelFactory, PositionFactory


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

    def test_create(self):
        PositionFactory.create()
        self.assertEqual(1, Position.objects.count())

    def test_create_temporary(self):
        tino_ns = OrganizationUnit.objects.get(slug='tino-ns')
        position = PositionFactory.create_temporary_position(current_office=tino_ns)
        self.assertEqual(position.tenure, Position.TEMPORARY_TENURE)
        self.assertIsNone(position.current_owner)
        self.assertEqual(tino_ns.slug, position.current_office.slug)


class TestPositionAssignment(TestCase):

    def test_create(self):
        employee = EmployeeFactory.create()
        position = PositionFactory.create()
        start_date = date(2015, 10, 1)
        end_date = date(2016, 9, 30)
        PositionEmployeeAssignment.objects.create(employee=employee,
                                                  position=position,
                                                  planned_start_date=start_date,
                                                  planned_end_date=end_date)
        self.assertEqual(1, PositionEmployeeAssignment.objects.count())

    def test_create_temporay_assignment_without_planned_dates(self):
        employee = EmployeeFactory.create()
        position = PositionFactory.create(tenure=Position.TEMPORARY_TENURE)
        start_date = date(2015, 10, 1)
        end_date = date(2016, 9, 30)
        try:
            assignment = PositionEmployeeAssignment.objects.create(employee=employee, position=position)
            self.fail('Did not raise exception')
        except ValueError as e:
            self.assertTrue(str(e).startswith('Temporary position assignmentes require planned start and end data.'))
        #assignment.save()
        self.assertEqual(0, PositionEmployeeAssignment.objects.count())

    def test_create_temporay_assignment_wrong_planned_dates(self):
        employee = EmployeeFactory.create()
        position = PositionFactory.create(tenure=Position.TEMPORARY_TENURE)
        end_date = date(2015, 10, 1)
        start_date = date(2016, 9, 30)
        try:
            PositionEmployeeAssignment.objects.create(employee=employee,
                                                      position=position,
                                                      planned_start_date=start_date,
                                                      planned_end_date=end_date)
            self.fail('Did not raise exception')
        except ValueError as e:
            self.assertTrue(str(e).startswith('Planned end date needs to be greater than start date.'))
        # assignment.save()
        self.assertEqual(0, PositionEmployeeAssignment.objects.count())
