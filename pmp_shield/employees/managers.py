from acp_calendar.models import FiscalYear
from django.db.models import Manager, Q
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

    def assigned_on_fiscal_year_to(self, fiscal_year, office):
        from .models import UnitAssignment
        assignments_query = UnitAssignment.objects.get_fiscal_year_assignments_to(fiscal_year, office).only('employee__id')
        return self.filter(id__in=assignments_query)

    def currently_assigned_to(self, office):
        from .models import UnitAssignment
        assignments_query = UnitAssignment.objects.get_current_assignments_to(office).only('employee__id')
        return self.filter(id__in=assignments_query)

class UnitAssignmentManager(Manager):

    def get_current_assignment(self, employee):
        return self.get(employee=employee, end_date__isnull=True)

    def get_current_assignments_to(self, office):
        return self.filter(office=office, end_date__isnull=True)

    def get_fiscal_year_assignments_to(self, fiscal_year, office):
        fiscal_year = FiscalYear(fiscal_year)
        # Got assigned during current FY and moved during current FY
        condition1 = Q(office=office,
                       start_date__range=(fiscal_year.start_date, fiscal_year.end_date),
                       end_date__range=(fiscal_year.start_date, fiscal_year.end_date))
        # Got the assingment on current FY and currently assigned to it
        condition2 = Q(office=office,
                       start_date__range=(fiscal_year.start_date, fiscal_year.end_date),
                       end_date__isnull=True)
        # Got the assignment on previous FY and currently assigne to it
        condition3 = Q(office=office, start_date__lte=fiscal_year.start_date,
                       end_date__isnull=True)
        # Got the assignment on previous FY and moved on current FY
        condition4 = Q(office=office, start_date__gte=fiscal_year.start_date,
                       end_date__range=(fiscal_year.start_date, fiscal_year.end_date))
        return self.filter(condition1|condition2|condition3|condition4)
