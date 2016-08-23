from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings

from django.conf import settings

from pmp_shield.employees.tests.factories import EmployeeFactory
from pmp_shield.users.tests.factories import UserFactory
from pmp_shield.employees.models import Employee


@override_settings(AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
))
class TestEmployeeListView(TestCase):

    def setUp(self):
        self.admin_user = UserFactory.create(username='batman', password='batman', is_staff=True)

    def test_get_employee_list(self):
        EmployeeFactory.create_batch(2)
        self.assertEqual(2, Employee.objects.count())
        is_logged = self.client.login(username=self.admin_user.username, password='batman')
        self.assertTrue(is_logged)
        url = reverse('employees:employee-list')
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)


