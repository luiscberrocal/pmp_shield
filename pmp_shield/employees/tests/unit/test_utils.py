import os
from unittest import mock
from unittest.mock import Mock

from django.conf import settings
from django.test import TestCase

from ....users.tests.factories import UserFactory
from ...utils import employee_selection_util
from ..mock_objects import MockLDAPTool


class TestEmployeeSelectionUtil(TestCase):

    @classmethod
    def setUpTestData(cls):
        filename = os.path.join(settings.TEST_DATA_PATH, 'ldap_data_marvel.xlsx')
        cls.mock_ldap_tool = MockLDAPTool(filename)

    def test_get_current_employee(self):
        user = UserFactory.create(username='cxavier')
        request = Mock()
        request.session = dict()
        request.user = user
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                        TestEmployeeSelectionUtil.mock_ldap_tool.search_by_username):
            employee = employee_selection_util.get_current_employee(request)
            self.assertEqual(employee.username, 'cxavier')

    def test_get_current_employee_none(self):
        user = UserFactory.create(username='batman')
        request = Mock()
        request.session = dict()
        request.user = user
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                        TestEmployeeSelectionUtil.mock_ldap_tool.search_by_username):
            employee = employee_selection_util.get_current_employee(request)
            self.assertIsNone(employee)

