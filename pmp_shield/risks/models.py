from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from ..projects.models import Project


class Risk(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    display_order = models.IntegerField(_('Diplay order'), default=1)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='risks')

    def __str__(self):
        return self.name
