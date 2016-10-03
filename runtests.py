import os
import sys

from django.conf import settings
from django.test.utils import get_runner

def run_tests(*test_args):
    #test pmp_shield.employees.tests.unit pmp_shield.common pmp_shield.projects.tests.unit pmp_shield.positions.tests.unit
    if not test_args:
        test_args = ['pmp_shield.employees.tests.unit',
                     'pmp_shield.achievements.tests.unit',
                     'pmp_shield.common',
                     'pmp_shield.goals.tests.unit',
                     'pmp_shield.positions.tests.unit',
                     'pmp_shield.projects.tests.unit',
                     'pmp_shield.risks.tests.unit',
                     'pmp_shield.users.tests',
                     ]
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.test'
    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()
    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
