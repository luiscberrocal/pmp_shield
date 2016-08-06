import base64

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
        content = StringIO()
        call_command('create_employee', usernames=['lberrocal', 'vjaen'], stdout=content)
        results = self.get_results(content)

        self.assertEqual(2, Employee.objects.count())
        self.assertEqual(2, len(results))

    def test_create_employee_doesnot_exist_in_ldap(self):
        content = StringIO()
        call_command('create_employee', usernames=['dad'], stdout=content)
        results = self.get_results(content)

        self.assertEqual(0, Employee.objects.count())
        self.assertEqual('Could not create employee for username dad', results[0])

    def test_get_photo_webservice_no_photo(self):
        ip = '1795341A'
        request = requests.get('http://10.1.92.213:18134/ords/vtmsapi/employee/%s/photo/' %(ip))
        self.assertEqual(404, request.status_code)

    def test_get_photo_webservice(self):
        ip = '1795341'
        request = requests.get('http://10.1.92.213:18134/ords/vtmsapi/employee/%s/photo/' % (ip))
        if request.status_code == 200:
            with open('./output/%s.jpg' % ip, 'wb') as image_file:
                image_file.write(request.content)
            base64_image = base64.b64encode(request.content).decode('utf-8')
            self.assertTrue(base64_image.startswith('/9j/4AAQSkZJRgABAQEA5gDmAAD/4QBSRXhpZgAAS'))
        else:
            self.fail('Could not connect to web service got %d status code' % request.status_code)



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
