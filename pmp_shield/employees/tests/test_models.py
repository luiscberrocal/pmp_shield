import datetime
from unittest import mock
from unittest.mock import Mock
import base64
import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.db.utils import IntegrityError

import logging

from .factories import EmployeeFactory
from ..models import OrganizationUnit, Phone, Employee

logger = logging.getLogger(__name__)


class TestOrganizationUnit(TestCase):
    def test_load(self):
        op = OrganizationUnit.objects.get(short_name='OP')
        opt = OrganizationUnit.objects.get(short_name='OPT')
        self.assertEqual(22, OrganizationUnit.objects.count())
        self.assertEqual(4, len(op.offices.all()))
        self.assertEqual(4, len(opt.offices.all()))


class TestACPEmployee(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        with open("./pmp_shield/employees/tests/fixtures/linux.jpeg", "rb") as imageFile:
            cls.photo_bytes = imageFile.read()

    def setUp(self):
        self.data = {'company_id': '1865325',
                     'first_name': 'Vasco',
                     'last_name': 'Nuñez de Balboa',
                     'username': 'vnunez',
                     'email': 'vnunez@pancanal.com',
                     'office': OrganizationUnit.objects.get(short_name='OPT')}

    def test_create(self):
        employee = Employee.objects.create(**self.data)
        self.assertIsNotNone(employee.pk)

    def test_create_with_factory(self):
        employee = EmployeeFactory.create()
        self.assertIsNotNone(employee.pk)
        self.assertEqual(1, Employee.objects.count())
        self.assertEqual(1, employee.phones.count())

    def test_create_with_factory_batch(self):
        EmployeeFactory.create_batch(10)
        self.assertEqual(10, Employee.objects.count())


    def test_photo_load(self):
        employee = Employee.objects.create(**self.data)
        photo_name = '%s.jpg' % employee.username
        employee.photo = SimpleUploadedFile(name=photo_name, content=self.photo_bytes, content_type='image/jpeg')
        employee.save()
        self.assertEqual('/media/photos/%s' % photo_name, employee.photo_url)
        self.assertTrue(os.path.exists(employee.photo.path))
        os.remove(employee.photo.path)


    @mock.patch('requests.get')
    @mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username')
    def test_get_or_create_from_username_create(self, mock_search_by_username, mock_get):
        response = Mock()
        response.status_code = 200
        photo_bytes_array = bytearray(self.photo_bytes)
        expected_image = "data:image/jpg;base64,%s" % base64.b64encode(photo_bytes_array).decode('utf-8')
        response.content = photo_bytes_array
        mock_get.return_value = response
        ldap_data = {'company_id': '1865325',
                     'first_name': 'Luis',
                     'last_name': 'Berrocal Cordoba',
                     'username': 'lberrocal',
                     'email': 'lberrocal@pancanal.com',
                     'office': 'TINO-NS',
                     'phone': '272-4149'}
        mock_search_by_username.return_value = [ldap_data]

        employee, created = Employee.objects.get_or_create_from_username('lberrocal')
        self.assertEqual('Luis', employee.first_name)
        self.assertEqual('Berrocal Cordoba', employee.last_name)
        self.assertEqual('272-4149', employee.phones.first().phone_number)
        self.assertEqual(1, Employee.objects.count())
        self.assertEqual(expected_image, employee.photo_url)
        self.assertTrue(created)

    @mock.patch('requests.get')
    @mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username')
    def test_get_or_create_from_username_create_contractor(self, mock_search_by_username, mock_get):
        response = Mock()
        response.status_code = 404
        mock_get.return_value = response
        ldap_data = {'company_id': '',
                     'first_name': 'Victor',
                     'last_name': 'Murillo',
                     'username': 'cont-vmurillo',
                     'email': 'cont-vmurillo@pancanal.com',
                     'office': None,
                     'phone': '272-4147'}

        mock_search_by_username.return_value = [ldap_data]
        employee, created = Employee.objects.get_or_create_from_username('cont-vmurillo')
        self.assertEqual('Victor', employee.first_name)
        self.assertEqual('272-4147', employee.phones.first().phone_number)
        self.assertEqual(1, Employee.objects.count())
        self.assertEqual(None, employee.photo_url)
        self.assertTrue(created)

    @mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username')
    def test_get_or_create_from_username_no_username(self, mock_search_by_username):
        mock_search_by_username.return_value = []

        employee, created = Employee.objects.get_or_create_from_username('invaliduser')
        self.assertIsNone(employee)
        self.assertFalse(created)

    @mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username')
    def test_get_or_create_from_username_get(self, mock_search_by_username):
        mock_search_by_username.return_value = []

        Employee.objects.create(**self.data)
        employee, created = Employee.objects.get_or_create_from_username('vnunez')
        self.assertEqual('Vasco', employee.first_name)
        self.assertEqual(1, Employee.objects.count())
        self.assertFalse(created)

    @mock.patch('pmp_shield.employees.ldap_tools.LDAPTool.search_by_username')
    def test_get_or_create_from_username_create_no_office(self, mock_search_by_username):
        ldap_data = {'company_id': None,
                     'first_name': 'Victor',
                     'last_name': 'Murillo',
                     'username': 'cont-vmurillo',
                     'email': 'cont-vmurillo@pancanal.com',
                     'office': 'IAIT-TOP',
                     'phone': None}

        mock_search_by_username.return_value = [ldap_data]
        try:
            employee, created = Employee.objects.get_or_create_from_username('jhuertas')
            self.fail('IAIT-TOP has not been created')
        except ValueError as e:
            self.assertEqual('There is no office for letters "IAIT-TOP"', str(e))

    def test_clean_invalid_company_id(self):
        self.data['company_id']= '186'
        employee = Employee.objects.create(**self.data)
        try:
            employee.full_clean()
            self.fail('Should have thrown a validation error')
        except ValidationError as e:
            self.assertEqual('company_id must have seven digits', e.message_dict['company_id'][0])

    def test_clean_no_office_with_valid_ip(self):
        self.data['office'] = None
        employee = Employee.objects.create(**self.data)
        try:
            employee.full_clean()
            self.fail('Should have thrown a validation error')
        except ValidationError as e:
            self.assertEqual('office cannot be null if company_id is valid', e.message_dict['office'][0])

    def test_clean_no_ip_with_valid_office(self):
        self.data['company_id'] = None

        try:
            employee = Employee.objects.create(**self.data)
            employee.full_clean()
            self.fail('Should have thrown a validation error')
        except IntegrityError as e:
            msg = str(e).split('\n')[0]
            self.assertEqual('null value in column "company_id" violates not-null constraint', msg)
