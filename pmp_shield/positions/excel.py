from openpyxl import load_workbook

from .models import GradeLevel, PositionDescription, Position, PositionEmployeeAssignment
from ..employees.models import OrganizationUnit, Employee
import logging

logger = logging.getLogger(__name__)

def import_positions_from_excel(filename):
    UNIT = 0
    PD = 1
    GRADE = 2
    LEVEL = 3
    TENURE = 4
    NUMBER = 5
    OWNER = 6
    TP = 7
    START = 8
    END = 9
    workbook = load_workbook(filename)
    sheet = workbook.active
    row_num=0
    for row in sheet.rows:
        if row_num != 0:
            try:
                office = OrganizationUnit.objects.get(short_name=row[UNIT].value)
            except OrganizationUnit.DoesNotExist:
                raise ValueError('Could not find an office with short name "%s" on row %d' % (row[UNIT].value, row_num))
            employee, _ = Employee.objects.get_or_create_from_username(row[OWNER].value)
            grade = GradeLevel.objects.get(grade_type=row[GRADE].value, level=row[LEVEL].value)
            #logger.debug('PD Short name: %s' % row[1].value)
            pd = PositionDescription.objects.get(short_name=row[PD].value)
            try:
                position = Position.objects.get(number=row[NUMBER].value)
            except Position.DoesNotExist:
                position = Position(number=row[NUMBER].value)

            position.grade = grade
            position.tenure = row[TENURE].value
            position.position_description = pd
            position.current_owner = employee
            position.current_office = office
            position.save()

            logger.debug('%02d %s %s %s %s' % (row_num, office.short_name, grade, position.tenure, employee,))
            if row[TP].value:
                employee, _ = Employee.objects.get_or_create_from_username(row[TP].value.lower())
                if not employee:
                    raise ValueError('Could not get empoyee for username %s' % row[TP].value)
                PositionEmployeeAssignment.objects.create(employee=employee, position=position,
                                                      planned_start_date=row[START].value,
                                                      planned_end_date=row[END].value)
                logger.debug('   Assigned %s' % (employee))
        row_num += 1
    return row_num


