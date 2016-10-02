import os
from unittest import mock
from unittest.mock import Mock

from django.conf import settings
from django.test import TestCase

from ...utils import employee_selection_util
from ..mock_objects import MockLDAPTool
from ....users.tests.factories import UserFactory
from ...middlewares import AutoSelectEmployeeMiddleware


class TestAutoSelectEmployeeMiddleware(TestCase):

    @classmethod
    def setUpTestData(cls):
        filename = os.path.join(settings.TEST_DATA_PATH, 'ldap_data_marvel.xlsx')
        cls.mock_ldap_tool = MockLDAPTool(filename)

    def setUp(self):
        self.middleware = AutoSelectEmployeeMiddleware()

    def test_process_request(self):
        user = UserFactory.create(username='cxavier')
        request = Mock()
        request.session = dict()
        request.user = user
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                        TestAutoSelectEmployeeMiddleware.mock_ldap_tool.search_by_username):
            self.middleware.process_request(request)
            self.assertEqual(request.session[employee_selection_util.selected_employee_key], 'cxavier')

