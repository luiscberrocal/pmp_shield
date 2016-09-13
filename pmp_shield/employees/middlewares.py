from .utils import employee_selection_util


class AutoSelectEmployeeMiddleware(object):

    def process_request(self, request):
        if not request.user or not request.user.is_authenticated():
            return
        employee_selection_util.get_current_employee(request)
