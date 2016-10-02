from .models import Employee


class EmployeeSelectionUtil(object):
    selected_employee_key = 'selected_employee_username'

    def get_current_employee(self, request):
        employee = None
        if self.selected_employee_key not in request.session:
            if request.user:
                employee, _ = Employee.objects.get_or_create_from_username(request.user.username)
                if employee:
                    request.session[self.selected_employee_key] = employee.username
        else:
            username = request.session[self.selected_employee_key]
            employee = Employee.objects.get(username=username)
        return employee

employee_selection_util = EmployeeSelectionUtil()
