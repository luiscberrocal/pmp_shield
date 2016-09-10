import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings

from django.conf import settings

from ..factories import EmployeeFactory, UnitAssignmentFactory
from ....users.tests.factories import UserFactory
from ...models import Employee, OrganizationUnit


@override_settings(AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
))
class TestEmployeeListView(TestCase):

    def setUp(self):
        self.admin_user = UserFactory.create(username='batman', password='batman', is_staff=True)
        self.tino_ns_office = OrganizationUnit.objects.get(short_name='TINO-NS')
        tino_ss_factory = OrganizationUnit.objects.get(short_name='TINO-SS')

        start_date = datetime.date(2015, 10, 1)
        end_date = start_date + datetime.timedelta(days=60)
        # Create 3 Assignments for TINO-NS that start on FY16 and end on same fiscal year
        UnitAssignmentFactory.create_batch(3, office=self.tino_ns_office, start_date=start_date, end_date=end_date)
        # Create 3 Assignments for TINO-NS that start on FY16 and have not ended yet
        UnitAssignmentFactory.create_batch(3, office=self.tino_ns_office, start_date=start_date)
        # Create 5 Assignments for TINO-SS that start on FY16 and have not ended yet
        UnitAssignmentFactory.create_batch(4, office=tino_ss_factory, start_date=start_date)
        start_date = datetime.date(2015, 10, 1) - datetime.timedelta(days=90)
        # Create 2 Assignments for TINO-NS that start on FY15 and have not ended yet
        UnitAssignmentFactory.create_batch(2, office=self.tino_ns_office, start_date=start_date)
        end_date = start_date + datetime.timedelta(days=60)
        # Create 8 Assignments for TINO-NS that start on FY15 and end on FY15
        UnitAssignmentFactory.create_batch(8, office=self.tino_ns_office, start_date=start_date, end_date=end_date)


    def test_get_employee_list(self):
        EmployeeFactory.create_batch(2)
        self.assertEqual(22, Employee.objects.count())
        is_logged = self.client.login(username=self.admin_user.username, password='batman')
        self.assertTrue(is_logged)
        url = reverse('employees:employee-list')
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Employees</h2>')
        self.assertContains(response, '<h4 class="list-group-item-heading">', count=22)


    def test_employee_list_assigned(self):
        self.assertEqual(20, Employee.objects.count())
        self.assertEqual(8, Employee.objects.currently_assigned_to(self.tino_ns_office).count())
        is_logged = self.client.login(username=self.admin_user.username, password='batman')
        self.assertTrue(is_logged)
        url = reverse('employees:employee-list-assigned', kwargs={'office_slug': 'tino-ns'})
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Employees Unidad de Nuevas Soluciones (TINO-NS)</h2>')
        self.assertContains(response, '<h4 class="list-group-item-heading">', count=8)


