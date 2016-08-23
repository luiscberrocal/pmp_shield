import base64
from unittest import mock

from django.test import TestCase

import requests
import re
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from pmp_shield.employees.models import Employee, UnitAssignment


class TestCreateEmployeeCommand(TestCase):

    def test_create_employee(self):
        def my_search_by_username(myself, username):
            ldap_data_lberrocal = [{'company_id': '1865325',
                                   'first_name': 'Luis',
                                   'last_name': 'Berrocal',
                                   'username': 'lberrocal',
                                   'email': 'lberrocal@pancanal.com',
                                   'office': 'TINO-NS',
                                   'phone': '272-4149'}]
            ldap_data_vjaen = [{'company_id': '1234567',
                               'first_name': 'Víctor',
                               'last_name': 'Jaen',
                               'username': 'vjaen',
                               'email': 'vjaen@pancanal.com',
                               'office': 'TINO-NS',
                               'phone': '272-4148'}]
            if username == 'lberrocal':
                return ldap_data_lberrocal
            else:
                return ldap_data_vjaen
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username', my_search_by_username):
            content = StringIO()
            call_command('create_employee', usernames=['lberrocal', 'vjaen'], stdout=content)
            results = self.get_results(content)

            self.assertEqual(2, Employee.objects.count())
            self.assertEqual('Berrocal', Employee.objects.get(username='lberrocal').last_name)
            self.assertEqual('Jaen', Employee.objects.get(username='vjaen').last_name)
            self.assertEqual(2, len(results))

    def test_create_employee_doesnot_exist_in_ldap(self):
        def my_search_by_username(myself, username):
            return []
        with mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username', my_search_by_username):
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
