from auditlog.models import AuditlogHistoryField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from ..employees.models import Employee
from ..projects.models import Project


class Goal(TimeStampedModel):
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name='goals', null=True, blank=True)
    expected_advancement = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)], default=0.9)
    expectations = models.TextField(null=True, blank=True)
    history = AuditlogHistoryField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.project is not None and self.pk is None:
            self.name = self.project.name
            self.description = self.project.description
        return super(Goal, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                      update_fields=update_fields)

    def __str__(self):
        return self.name


class ExpectationsList(TimeStampedModel):
    version = models.IntegerField(default=1)
    employee = models.ForeignKey(Employee, related_name='expectations_list')
    delivery_date = models.DateField(null=True, blank=True)
    fiscal_year = models.CharField(max_length=4,
                                   validators=[RegexValidator(regex=r'^AF\d{2}$',
                                                              message=_('Fiscal year must use format AFYY. '
                                                                        'For example AF16 for fiscal year 2016'))])

    class Meta:
        unique_together = ('version', 'employee', 'fiscal_year')


class EmployeeGoal(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='employee_goals')
    goal = models.ForeignKey(Goal, related_name='employee_goals')
    expectations = models.TextField(null=True, blank=True)
    weight = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    expectations_list = models.ForeignKey(ExpectationsList, related_name='employee_goals')
    history = AuditlogHistoryField()

    class Meta:
        unique_together = ('employee', 'goal', 'expectations_list')

    def __str__(self):
        return '%s - %s' % (self.employee, self.goal)







