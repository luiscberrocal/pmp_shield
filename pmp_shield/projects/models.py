from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

# Create your models here.
from django.db.models import Q
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from ..employees.models import Employee, OrganizationUnit


class Project(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=120)
    sponsor = models.ForeignKey(Employee, verbose_name=_('Sponsor'), related_name='sponsored_projects')
    project_manager = models.ForeignKey(Employee, verbose_name=('Project Manager'), related_name='managed_projects')
    justification = models.TextField(_('Justification'))
    scope = models.TextField(_('Scope'))
    office = models.ForeignKey(OrganizationUnit, verbose_name=_('office in charge'),
                               blank=True, null=True, related_name='projects')

    history = AuditlogHistoryField()

    def start_end_dates(self):
        milestones = self.milestones.filter(Q(milestone_type=Milestone.MILESTONE_START)|
                                       Q(milestone_type=Milestone.MILESTONE_END))
        if len(milestones) == 2 and (milestones[0].milestone_type == Milestone.MILESTONE_START or
            milestones[1].milestone_type == Milestone.MILESTONE_END):
            return milestones[0].date, milestones[1].date
        elif len(milestones) == 1 and milestones[0].milestone_type == Milestone.MILESTONE_START:
            return milestones[0].date, None
        else:
            None, None

    def __str__(self):
        return self.name


class Assumption(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    display_order = models.IntegerField(_('Diplay order'), default=1)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='assumptions')
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('display_order',)

class Restriction(TimeStampedModel):
    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'))
    display_order = models.IntegerField(_('Diplay order'), default=1)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='restrictions')
    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('display_order',)


class Milestone(TimeStampedModel):
    MILESTONE_START = 'START'
    MILESTONE_END = 'END'
    MILESTONE_OTHER = 'OTHER'
    MILESTONE_TYPES = ((MILESTONE_START, _('Start')),
                       (MILESTONE_END, _('End')),
                       (MILESTONE_OTHER, _('Other')))

    name = models.CharField(_('Name'),max_length=120)
    description = models.TextField(_('Description'), blank=True)
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='milestones')
    date = models.DateField(_('Date'))
    milestone_type = models.CharField(max_length=5, verbose_name=_('Milestone type'),
                                      choices=MILESTONE_TYPES, default=MILESTONE_OTHER)

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date',)


class ProjectMembership(TimeStampedModel):
    MEMBER_ROLE = 'MEMBER'
    LEADER_ROLE = 'LEADER'
    ROLES = ((MEMBER_ROLE, _('Member')),
             (LEADER_ROLE, _('Leader')))
    member = models.ForeignKey(Employee, related_name='projects', verbose_name=_('Member'))
    project = models.ForeignKey(Project, related_name='members', verbose_name=_('Project'))
    role = models.CharField(max_length=6, choices=ROLES, default=MEMBER_ROLE)


auditlog.register(Project)
auditlog.register(Assumption, exclude_fields=['display_order'])
auditlog.register(Restriction, exclude_fields=['display_order'])
auditlog.register(Milestone)
