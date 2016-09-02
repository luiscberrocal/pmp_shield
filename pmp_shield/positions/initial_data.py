from pmp_shield.employees.models import OrganizationUnit
from .models import GradeLevel, PositionDescription, Position


def create_grades():
    GradeLevel.objects.create(grade_type='NM', level=7)
    GradeLevel.objects.create(grade_type='NM', level=9)
    GradeLevel.objects.create(grade_type='NM', level=11)
    GradeLevel.objects.create(grade_type='NM', level=12)
    GradeLevel.objects.create(grade_type='NM', level=13)
    GradeLevel.objects.create(grade_type='NM', level=14)

def create_pds():
    PositionDescription.objects.create(name='Esp en Informática (Des Sof/Ana Sist)', short_name='Analista')
    PositionDescription.objects.create(name='Esp en Informática (Des Soft)', short_name='Desarrollador')
    PositionDescription.objects.create(name='Esp en Informática', short_name='Especialista')
    PositionDescription.objects.create(name='Supv, Especialista en Informática', short_name='Supervisor')
    PositionDescription.objects.create(name='Gerente', short_name='Gerente')

def create_positions():
    office = OrganizationUnit.objects.get(slug='tino-ns')

    grade = GradeLevel.objects.get(grade_type='NM', level=12)
    pd = PositionDescription.objects.get(short_name='Analista')
    positions = ['120204', '120332', '120191']
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.PERMANENT_TENURE,
                                position_description=pd, current_office=office)

    grade = GradeLevel.objects.get(grade_type='NM', level=11)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['120216', '120217', '120220', '120197', ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.PERMANENT_TENURE,
                                position_description=pd, current_office=office)

    grade = GradeLevel.objects.get(grade_type='NM', level=9)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['128117', '128116', '128144', '120534']
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.PERMANENT_TENURE,
                                position_description=pd, current_office=office)

    grade = GradeLevel.objects.get(grade_type='NM', level=7)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['120583',]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.PERMANENT_TENURE,
                                position_description=pd, current_office=office)

    grade = GradeLevel.objects.get(grade_type='NM', level=11)
    pd = PositionDescription.objects.get(short_name='Especialista')
    positions = ['120580', ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.PERMANENT_TENURE,
                                position_description=pd, current_office=office)
    # NM-12 TEMPORAL ANALISTA
    grade = GradeLevel.objects.get(grade_type='NM', level=12)
    pd = PositionDescription.objects.get(short_name='Analista')
    positions = ['120727', '120831', ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.TEMPORARY_TENURE,
                                position_description=pd, current_office=office)

    # NM-11 TEMPORAL DESARROLLADOR
    grade = GradeLevel.objects.get(grade_type='NM', level=11)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['120829',  ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.TEMPORARY_TENURE,
                                position_description=pd, current_office=office)
    # NM-09 TEMPORAL DESARROLLADOR
    grade = GradeLevel.objects.get(grade_type='NM', level=9)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['120730', '120736', ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.TEMPORARY_TENURE,
                                position_description=pd, current_office=office)
    # NM-09 TEMPORAL DESARROLLADOR
    grade = GradeLevel.objects.get(grade_type='NM', level=7)
    pd = PositionDescription.objects.get(short_name='Desarrollador')
    positions = ['120732', ]
    for pos in positions:
        Position.objects.create(grade=grade, number=pos, tenure=Position.TEMPORARY_TENURE,
                                position_description=pd, current_office=office)


