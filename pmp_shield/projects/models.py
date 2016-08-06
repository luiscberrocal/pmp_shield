from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from ..employees.models import Employee


class Project(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=120)
    sponsor = models.ForeignKey(Employee, verbose_name=_('Sponsor'), related_name='sponsored_projects')
    project_manager = models.ForeignKey(Employee, verbose_name=('Project Manager'), related_name='pm_projects')
    justification = models.TextField(_('Justification'))
    scope = models.TextField(_('Scope'))

    def __str__(self):
        return self.name


class Assumption(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    display_order = models.IntegerField(_('Diplay order'), default=1)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='assumptions')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('display_order',)

class Restriction(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    display_order = models.IntegerField(_('Diplay order'), default=1)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='restrictions')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('display_order',)


class Milestones(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='milestones')
    date = models.DateField(_('Date'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date',)
