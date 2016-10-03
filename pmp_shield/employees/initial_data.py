import datetime

from .models import OrganizationUnit


def create_acp_organization():
    acp = OrganizationUnit.objects.create(name='Autoridad del Canal de Panamá', short_name='ACP')
    op = OrganizationUnit.objects.create(name='Vicepresidencia Ejecutiva de Operaciones',
                                         short_name='OP', parent=acp)

    op_divisions = [OrganizationUnit(name='División de Operaciones de Tránsito', short_name='OPT', parent=op),
                    OrganizationUnit(name='División de Recursos de Tránsito', short_name='OPR', parent=op),
                    OrganizationUnit(name='División de Dragados', short_name='OPD', parent=op),
                    OrganizationUnit(name='División de Protección y Respuestas a Emergencias', short_name='OPP',
                                     parent=op)]
    for division in op_divisions:
        division.save()

    opt = OrganizationUnit.objects.get(short_name='OPT')
    opt_sections = [OrganizationUnit(name='Sección de Capitanía de Puerto, Norte', short_name='OPTN', parent=opt),
                    OrganizationUnit(name='Sección de Capitanía de Puerto, Sur', short_name='OPTS', parent=opt),
                    OrganizationUnit(name='Sección de Prácticos', short_name='OPTP', parent=opt),
                    OrganizationUnit(name='Sección de Tráfico Marítimo y Arqueo', short_name='OPTC', parent=opt),]

    for section in opt_sections:
        section.save()

    ti = OrganizationUnit.objects.create(name='Vicepresidencia Ejecutiva de Tecnología e Informática',
                                         short_name='TI', parent=acp)
    ti_divisions = [OrganizationUnit(name='División de Infraestructura y Operaciones Tecnológicas', short_name='TIO', parent=ti),
                    OrganizationUnit(name='División de Servicios y Recursos Tecnológicos', short_name='TIS', parent=ti),
                    OrganizationUnit(name='División de Ingeniería de Soluciones Tecnológicas', short_name='TIN', parent=ti),
                    OrganizationUnit(name='Programa de Renovación Tecnológica (RENOVA)', short_name='TIRE',
                                     parent=ti)]
    for division in ti_divisions:
        division.save()

    tin = OrganizationUnit.objects.get(short_name='TIN')
    tin_sections = [OrganizationUnit(name='Sección Soluciones de Gestión Administrativa', short_name='TINA', parent=tin),
                    OrganizationUnit(name='Sección de Gestión Operacional', short_name='TINO', parent=tin),
                    OrganizationUnit(name='Unidad de Soluciones de Inteligencia de Negocios', short_name='TINN', parent=tin),
                    OrganizationUnit(name='Unidad de Proyectos de Soluciones Informáticas', short_name='TINS', parent=tin),
                    OrganizationUnit(name='Unidad de Soluciones de Información Geográfica', short_name='TING', parent=tin), ]

    for section in tin_sections:
        section.save()

    tino = OrganizationUnit.objects.get(short_name='TINO')
    tino_units = [OrganizationUnit(name='Unidad de Soluciones de Servicios Marítimos y Operacionales', short_name='TINO-SS', parent=tino),
                  OrganizationUnit(name='Unidad de Nuevas Soluciones', short_name='TINO-NS', parent=tino),
                  ]
    for unit in tino_units:
        unit.save()
