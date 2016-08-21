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

from pmp_shield.employees.tests.factories import EmployeeFactory, UnitAssignmentFactory
from pmp_shield.employees.models import OrganizationUnit, Phone, Employee, UnitAssignment

logger = logging.getLogger(__name__)


class TestOrganizationUnit(TestCase):

    def test_load(self):
        op = OrganizationUnit.objects.get(short_name='OP')
        opt = OrganizationUnit.objects.get(short_name='OPT')
        self.assertEqual(22, OrganizationUnit.objects.count())
        self.assertEqual(4, len(op.offices.all()))
        self.assertEqual(4, len(opt.offices.all()))

    def test_slug(self):
        tino_ns = OrganizationUnit.objects.get(short_name='TINO-NS')
        self.assertEqual('tino-ns', tino_ns.slug)


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

    def test_assign_to_office(self):
        office = OrganizationUnit.objects.get(short_name='TINO-NS')
        new_office = OrganizationUnit.objects.get(short_name='TINO-SS')

        start_date = datetime.date(2016, 10, 1)
        assignment = UnitAssignmentFactory.create(office=office, start_date=start_date)
        new_assignment = assignment.employee.assign_to_office(new_office, start_date=datetime.date(2016, 12, 1))

        self.assertEqual(new_office, new_assignment.office)
        current_assignment = UnitAssignment.objects.get_current_assignment(employee=new_assignment.employee)
        self.assertEqual(new_office, current_assignment.office)

    def test_assign_to_office_wrong_start_date(self):
        office = OrganizationUnit.objects.get(short_name='TINO-NS')
        new_office = OrganizationUnit.objects.get(short_name='TINO-SS')

        start_date = datetime.date(2016, 10, 1)
        assignment = UnitAssignmentFactory.create(office=office, start_date=start_date)
        try:
            new_assignment = assignment.employee.assign_to_office(new_office, start_date=datetime.date(2016, 9, 1))
            self.fail('Should have sent an error')
        except ValueError as e:
            parts = str(e).split('.')
            self.assertEqual('Cannot start an assignment before previous one started', parts[0])
            self.assertEqual('Previous: Unidad de Nuevas Soluciones (TINO-NS), start date: 2016-10-01', parts[1].strip())
            self.assertEqual('Current: Unidad de Soluciones de Servicios Marítimos y Operacionales (TINO-SS), start date: 2016-09-01', parts[2].strip())

    def test_assign_to_office_wrong_start_date_2(self):
        office = OrganizationUnit.objects.get(short_name='TINO-NS')
        new_office = OrganizationUnit.objects.get(short_name='TINO-SS')

        start_date = datetime.date(2016, 10, 1)
        assignment = UnitAssignmentFactory.create(office=office, start_date=start_date)
        try:
            new_assignment = assignment.employee.assign_to_office(new_office, start_date=datetime.date(2016, 10, 1))
            self.fail('Should have sent an error')
        except ValueError as e:
            parts = str(e).split('.')
            self.assertEqual('Cannot start an assignment before previous one started', parts[0])
            self.assertEqual('Previous: Unidad de Nuevas Soluciones (TINO-NS), start date: 2016-10-01', parts[1].strip())
            self.assertEqual('Current: Unidad de Soluciones de Servicios Marítimos'
                             ' y Operacionales (TINO-SS), start date: 2016-10-01', parts[2].strip())


    def test_assign_to_office_no_previous_assignment(self):
        employee = EmployeeFactory.create()
        office = OrganizationUnit.objects.get(short_name='TINO-SS')

        start_date = datetime.date(2016, 10, 1)
        assignment = UnitAssignmentFactory.create(employee=employee, office=office, start_date=start_date)

        self.assertEqual(office, assignment.office)
        current_assignment = UnitAssignment.objects.get_current_assignment(employee=employee)
        self.assertEqual(office, current_assignment.office)



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

class TestUnitAssignment(TestCase):

    def test_create(self):
        assignment = UnitAssignmentFactory.create()
        self.assertEqual(1, UnitAssignment.objects.count())

    def test_get_current_assignment(self):
        office = OrganizationUnit.objects.get(short_name='TINO-NS')
        new_office = OrganizationUnit.objects.get(short_name='TINO-SS')
        last_office = OrganizationUnit.objects.get(short_name='OPT')

        start_date = datetime.date(2016, 10, 1)
        end_date = start_date + datetime.timedelta(days=180)
        assignment = UnitAssignmentFactory.create(office=office, start_date=start_date, end_date=end_date)

        start_date = end_date + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=60)
        UnitAssignmentFactory.create(office=new_office, employee=assignment.employee,
                                     start_date=start_date, end_date= end_date)

        start_date = end_date + datetime.timedelta(days=1)
        UnitAssignmentFactory.create(office=last_office, employee=assignment.employee, start_date=start_date)

        self.assertEqual(3, UnitAssignment.objects.filter(employee=assignment.employee).count())
        self.assertEqual(last_office, UnitAssignment.objects.get_current_assignment(employee=assignment.employee).office)




