import os

from django.core.management import BaseCommand
from django.conf import settings
import logging

from ...models import Employee

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage
        $ python manage.py create_employee -u oaherrera jduarte
    """

    def add_arguments(self, parser):
        #parser.add_argument('output_filename')
        parser.add_argument("-u", "--username",
                            dest="usernames",
                            help="LDAP usernames to create employees",
                            nargs='+',
                            )

    def handle(self, *args, **options):
        #path, file = os.path.split(options['output_filename'])
        for username in options['usernames']:
            employee, created = Employee.objects.get_or_create_from_username(username)
            if employee:
                self.stdout.write('Employee: %s created: %s' % (employee, created))
            else:
                self.stdout.write('Could not create employee for username %s' % username)
