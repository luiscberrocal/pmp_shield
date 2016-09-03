from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from pmp_shield.employees.models import Employee, OrganizationUnit


class GradeLevel(TimeStampedModel):
    grade_type = models.CharField(_('grade type'), max_length=2)
    level = models.IntegerField(_('level'))

    class Meta:
        ordering = ('grade_type', 'level')
        unique_together = ('grade_type', 'level')

    def __str__(self):
        return '%s-%02d' % (self.grade_type, self.level)


class PositionDescription(TimeStampedModel):
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Position(TimeStampedModel):
    PERMANENT_TENURE = 'P'
    TEMPORARY_TENURE = 'T'
    TENURE_TYPES = ((PERMANENT_TENURE, _('Permanent')),
                    (TEMPORARY_TENURE, _('Temporary')))
    grade = models.ForeignKey(GradeLevel, related_name='positions', verbose_name=_('grade'))
    number = models.CharField(_('position number'), max_length=6, unique=True)
    tenure = models.CharField(_('tenure'), max_length=1, choices=TENURE_TYPES, default=TEMPORARY_TENURE)
    position_description = models.ForeignKey(PositionDescription, related_name='positions',
                                             verbose_name=_('position description'))
    current_owner = models.OneToOneField(Employee, related_name='permanent_position',
                                         null=True, blank=True, verbose_name=_('current owner'))
    current_office = models.ForeignKey(OrganizationUnit, related_name='positions', verbose_name=_('current office'))

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return '%s %s %s' % (self.grade, self.number, self.tenure)


class PositionEmployeeAssignment(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='position_assignments')
    position = models.ForeignKey(Position, related_name='position_assignments')
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)


