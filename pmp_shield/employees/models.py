import base64
import re
from datetime import timedelta

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from .managers import EmployeeManager, UnitAssignmentManager


class OrganizationUnit(MPTTModel, TimeStampedModel):
    name = models.CharField(_('Office name'), max_length=120)
    short_name = models.CharField(_('Office Letters'), max_length=8, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='offices', db_index=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.short_name)



class Employee(TimeStampedModel):
    company_id = models.CharField(_('ACP IP'), max_length=7, blank=True)
    office = models.ForeignKey(OrganizationUnit, verbose_name=_('Office'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=60)
    middle_name = models.CharField(_('middle name'), max_length=60, blank=True)
    last_name = models.CharField(_('last name'), max_length=60)
    username = models.CharField(_('username'), max_length=35, unique=True)
    email = models.EmailField()
    phones = models.ManyToManyField('Phone', related_name='owner')
    photo = models.ImageField(upload_to='photos/', max_length=255,
                              blank=True, verbose_name=_('photo'))

    @property
    def photo_url(self):
        """
        Get the url from photo field if there is a photo loaded, if not, it returns the photo from the
        EVTMS database
        :return: photo url in a format an Html img tag can use
        """
        if self.photo:
            return self.photo.url
        else:
            request = requests.get(getattr(settings, 'HR_PHOTO_URL') % (self.company_id))
            if request.status_code == 200:
                base64_image = base64.b64encode(request.content).decode('utf-8')
                return "data:image/jpg;base64,%s" % base64_image

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    objects = EmployeeManager()

    def clean(self):
        if self.company_id is not None:
            # If company_id is not None it means its an ACP employee that requires an office and a company_id
            regexp = re.compile(r'\d{7}')
            if not regexp.match(self.company_id):
                raise ValidationError({'company_id': 'company_id must have seven digits'})
            if self.office is None:
                raise ValidationError({'office': 'office cannot be null if company_id is valid'})
        else:
            # If does not have a company then it is a contractor and should not have an office assigned
            if self.office is not None:
                raise ValidationError({'company_id': 'company_id cannot be null if office is valid'})

    def assign_to_office(self, office, start_date=timezone.now()):
        try:
            current_assignment = UnitAssignment.objects.get_current_assignment(employee=self)
            if current_assignment.start_date >= start_date:
                msg = 'Cannot start an assignment before previous one started. ' \
                      'Previous: %s, start date: %s. Current: %s, start date: %s'
                raise ValueError(msg % (current_assignment.office, current_assignment.start_date,
                                        office, start_date))
        except UnitAssignment.DoesNotExist:
            current_assignment = None
        if current_assignment:
            current_assignment.end_date = start_date - timedelta(days=1)
            current_assignment.save()
        assignment = UnitAssignment.objects.create(employee=self, start_date=start_date, office=office)
        return assignment




class Phone(TimeStampedModel):
    BUSINESS = 'BUSINESS'
    MOBILE = 'MOBILE'
    HOME = 'HOME'
    RADIO = 'RADIO'
    OTHER = 'OTHER'

    PHONE_TYPES = ((BUSINESS, _('Business')),
                   (MOBILE, _('Mobile')),
                   (HOME, _('Home')),
                   (RADIO, _('Radio')),
                   (OTHER, _('Other')),)

    phone_number = models.CharField(_('Phone number'), max_length=15)
    phone_type = models.CharField(_('Phone type'), max_length=8, choices=PHONE_TYPES, default=BUSINESS)

    def __str__(self):
        return '%s %s: %s' % (self.owner, self.phone_type, self.phone_number)

class UnitAssignment(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='assignments', verbose_name=_('Employee'))
    office = models.ForeignKey(OrganizationUnit, related_name='assignments', verbose_name=('Office'))
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    objects = UnitAssignmentManager()

