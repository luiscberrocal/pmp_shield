import os
from unittest import mock

from django.test import TestCase

from django.conf import settings

from ....employees.tests.mock_objects import MockLDAPTool
from ...models import Position
from ...excel import import_positions_from_excel


class TestExcel(TestCase):

    @classmethod
    def setUpTestData(cls):
        filename = os.path.join(settings.TEST_DATA_PATH, 'ldap_data_marvel.xlsx')
        cls.mock_ldap_tool = MockLDAPTool(filename)

    def test_import_positions_from_excel(self):
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                        TestExcel.mock_ldap_tool.search_by_username):
            filename = os.path.join(settings.TEST_DATA_PATH, 'positions_test_data.xlsx')
            import_positions_from_excel(filename)
            self.assertEqual(8, Position.objects.count())

