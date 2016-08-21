import base64
from unittest import mock

from django.test import TestCase

import requests
import re
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from ..models import Employee


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
