from pmp_shield.employees.models import OrganizationUnit, Employee
from .models import GradeLevel, PositionDescription, Position


def create_grades():
    GradeLevel.objects.create(grade_type='NM', level=7)
    GradeLevel.objects.create(grade_type='NM', level=9)
    GradeLevel.objects.create(grade_type='NM', level=11)
    GradeLevel.objects.create(grade_type='NM', level=12)
    GradeLevel.objects.create(grade_type='NM', level=13)
    GradeLevel.objects.create(grade_type='NM', level=14)

def create_pds():
    PositionDescription.objects.create(name='Esp en Informática (Des Sof/Ana Sist)', short_name='ANALISTA')
    PositionDescription.objects.create(name='Esp en Informática (Des Soft)', short_name='DESARROLLADOR')
    PositionDescription.objects.create(name='Esp en Informática', short_name='ESPECIALISTA')
    PositionDescription.objects.create(name='Supv, Especialista en Informática', short_name='SUPERVISOR')
    PositionDescription.objects.create(name='Gerente', short_name='GERENTE')

