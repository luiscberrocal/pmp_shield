from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from django.conf import settings
from ..models import Employee


class TestEmployeeListView(TestCase):

    def setUp(self):
        self.client = Client()
        Employee.objects.get_or_create_from_username('lberrocal')
        Employee.objects.get_or_create_from_username('oaherrera')

    def test_get_employee_list(self):
        self.assertEqual(2, Employee.objects.count())
        is_logged = self.client.login(username=getattr(settings, 'LDAP_USERNAME'), password=getattr(settings, 'LDAP_BIND_PWD'))
        self.assertTrue(is_logged)
        url = reverse('employees:employee-list')
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)


