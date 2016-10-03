import base64
import os
from unittest import mock

from django.test import TestCase

import requests
import re
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from pmp_shield.employees.models import Employee, UnitAssignment
from pmp_shield.employees.tests.mock_objects import MockLDAPTool


class TestCreateEmployeeCommand(TestCase):

    @classmethod
    def setUpTestData(cls):
        filename = os.path.join(settings.TEST_DATA_PATH, 'ldap_data_marvel.xlsx')
        cls.mock_ldap_tool = MockLDAPTool(filename)


    def test_create_employee(self):
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                            TestCreateEmployeeCommand.mock_ldap_tool.search_by_username):
            content = StringIO()
            call_command('create_employee', usernames=['pparker', 'bbanner'], stdout=content)
            results = self.get_results(content)

            self.assertEqual(2, Employee.objects.count())
            self.assertEqual('Parker', Employee.objects.get(username='pparker').last_name)
            self.assertEqual('Banner', Employee.objects.get(username='bbanner').last_name)
            self.assertEqual(2, len(results))

    def test_create_employee_doesnot_exist_in_ldap(self):
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username',
                        TestCreateEmployeeCommand.mock_ldap_tool.search_by_username):
            content = StringIO()
            call_command('create_employee', usernames=['dad'], stdout=content)
            results = self.get_results(content)

            self.assertEqual(0, Employee.objects.count())
            self.assertEqual('Could not create employee for username dad', results[0])

    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            employee_data = dict()
            regexp = r'^Employee:\s([\w\s,]+)\screated:\s(True|False)\n$'
            pattern = re.compile(regexp)
            match = pattern.match(line)
            if match:
                employee_data['name'] = match.group(1)
                employee_data['created'] = match.group(2)
                results.append(employee_data)
            else:
                results.append(line.strip('\n'))
        return results

class TestCreateFakeEmployeesCommand(TestCase):

    def test_create_random(self):
        content = StringIO()
        call_command('create_fake_employees', count='10', stdout=content)
        results = self.get_results(content)

        self.assertEqual(0, UnitAssignment.objects.count())
        self.assertEqual(10, Employee.objects.count())
        self.assertEqual(10, len(results))

    def test_create_for_office(self):
        content = StringIO()
        content2 = StringIO()
        call_command('create_fake_employees', count='10', office='TINO-NS', stdout=content)
        call_command('create_fake_employees', count='8', office='TINO-SS', stdout=content2)
        results = self.get_results(content)

        self.assertEqual(18, Employee.objects.count())
        self.assertEqual(0, UnitAssignment.objects.count())

        self.assertEqual(10, len(results))
        self.assertEqual(10, Employee.objects.filter(office__short_name='TINO-NS').count())

        results = self.get_results(content2)
        self.assertEqual(8, len(results))
        self.assertEqual(8, Employee.objects.filter(office__short_name='TINO-SS').count())

    def test_create_for_office_with_assignment(self):
        content = StringIO()
        call_command('create_fake_employees', count='10', office='TINO-NS',
                     assignment_date='2016-10-1', stdout=content)

        results = self.get_results(content)
        self.assertEqual(10, Employee.objects.count())
        self.assertEqual(10, len(results))
        self.assertEqual(10, UnitAssignment.objects.filter(office__short_name='TINO-NS').count())

    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results
