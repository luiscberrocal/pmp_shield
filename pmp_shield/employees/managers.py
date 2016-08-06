from django.db.models import Manager
from .ldap_tools import LDAPTool


class EmployeeManager(Manager):

        ldap = LDAPTool()

        def get_or_create_from_username(self, username):
            employee = None
            created = False

            employee_data = self.ldap.search_by_username(username)

            if len(employee_data) == 1:
                from .models import OrganizationUnit
                phone_number = employee_data[0].pop('phone', None)
                office = employee_data[0].pop('office', None)
                company = employee_data[0].pop('company', None)
                if office is not None:
                    try:
                        unit = OrganizationUnit.objects.get(short_name=office)
                    except OrganizationUnit.DoesNotExist:
                        raise ValueError('There is no office for letters "%s"' % office)
                    employee_data[0]['office'] = unit
                employee_data[0].pop('tenure', None)
                employee, created = self.get_or_create(**employee_data[0])
                if phone_number is not None:
                    from .models import Phone
                    phone = Phone.objects.create(phone_number=phone_number)
                    employee.phones.add(phone)
                    employee.save()
            elif len(employee_data) == 0:
                try:
                    employee = self.get(username=username)
                    return employee, False
                except self.model.DoesNotExist:
                    pass
            return employee, created

