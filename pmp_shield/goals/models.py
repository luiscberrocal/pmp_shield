from auditlog.models import AuditlogHistoryField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from ..employees.models import Employee
from ..projects.models import Project


class Goal(TimeStampedModel):
    name = models.CharField(_('name'), max_length=120, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=_('project'), null=True,
                                blank=True, related_name='goals')
    expected_advancement = models.FloatField(_('expected advancement'),
                                             validators=[MaxValueValidator(1.0),
                                             MinValueValidator(0.0)],
                                             default=0.9)
    expectations = models.TextField(_('expectations'), null=True, blank=True)
    history = AuditlogHistoryField(_('history'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.project is not None and self.pk is None:
            self.name = self.project.name
            self.description = self.project.description
        return super(Goal, self).save(force_insert=force_insert,
                                      force_update=force_update, using=using,
                                      update_fields=update_fields)

    def __str__(self):
        return self.name


class ExpectationsList(TimeStampedModel):
    version = models.IntegerField(_('version'), default=1)
    employee = models.ForeignKey(Employee, verbose_name=_('employee'),
                                 related_name='expectations_list')
    delivery_date = models.DateField(_('delivery date'), null=True, blank=True)
    fiscal_year = models.CharField(_('fiscal year'), max_length=4,
                                   validators=[RegexValidator(
                                   regex=r'^AF\d{2}$', message=_(
                                   'Fiscal year must use format AFYY. '
                                   'For example AF16 for fiscal year 2016'))])

    class Meta:
        unique_together = ('version', 'employee', 'fiscal_year')


class EmployeeGoal(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='employee_goals',
                                 verbose_name=_('employee'))
    goal = models.ForeignKey(Goal, related_name='employee_goals',
                             verbose_name=_('goal'))
    expectations = models.TextField(_('expectations'), null=True, blank=True)
    weight = models.FloatField(_('weight'), validators=[MaxValueValidator(1.0),
                               MinValueValidator(0.0)])
    expectations_list = models.ForeignKey(ExpectationsList,
                                          related_name='employee_goals',
                                          verbose_name=_('expectations list'))
    history = AuditlogHistoryField(_('history'))

    class Meta:
        unique_together = ('employee', 'goal', 'expectations_list')

    def __str__(self):
        return '%s - %s' % (self.employee, self.goal)

