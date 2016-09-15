from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from ..employees.models import Employee


class Achievement(TimeStampedModel):
    ACHIEVEMENT_TYPE = 'A'
    INITIATIVE_TYPE = 'I'
    ACHIEVEMENT_TYPES = ((ACHIEVEMENT_TYPE, _('Achievement')),
                         (INITIATIVE_TYPE, _('Initiative')))
    employee = models.ForeignKey(Employee, verbose_name=_('employee'),
                                 related_name='achievements')
    fiscal_year = models.IntegerField(_('fiscal year'))
    type = models.CharField(_('achievement type'), max_length=1, choices=ACHIEVEMENT_TYPES)
    description = models.TextField(_('description'))
    points = models.IntegerField(_('points'), null=True, blank=True,
                                 help_text='Points assigned by supervisor.'
                                           ' 0 to 5. 0 means not accepted, 5 means highest impact')

    def __str__(self):
        return '%s - %s' % (self.employee, self.description)
