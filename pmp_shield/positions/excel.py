from openpyxl import load_workbook

from .models import GradeLevel, PositionDescription, Position, PositionEmployeeAssignment
from ..employees.models import OrganizationUnit, Employee
import logging

logger = logging.getLogger(__name__)

def import_positions_from_excel(filename):
    workbook = load_workbook(filename)
    sheet = workbook.active
    row_num=0
    for row in sheet.rows:
        if row_num != 0:
            try:
                office = OrganizationUnit.objects.get(short_name=row[0].value)
            except OrganizationUnit.DoesNotExist:
                raise ValueError('Could not find an office with short name "%s" on row %d' % (row[0].value, row_num))
            employee, _ = Employee.objects.get_or_create_from_username(row[6].value)
            grade = GradeLevel.objects.get(grade_type=row[2].value, level=row[3].value)
            pd = PositionDescription.objects.get(short_name=row[1].value)
            position = Position.objects.create(grade=grade, number=row[5].value, tenure=row[4].value,
                                    position_description=pd, current_office=office,
                                    current_owner=employee)
            logger.debug('%02d %s %s %s %s' % (row_num, office.short_name, grade, position.tenure, employee,))
            if row[7].value:
                employee, _ = Employee.objects.get_or_create_from_username(row[7].value.lower())
                if not employee:
                    raise ValueError('Could not get empoyee for username %s' % row[7].value)
                PositionEmployeeAssignment.objects.create(employee=employee, position=position,
                                                      planned_start_date=row[8].value,
                                                      planned_end_date=row[9].value)
                logger.debug('   Assigned %s' % (employee))
        row_num += 1


