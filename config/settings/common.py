# -*- coding: utf-8 -*-
"""
Django settings for PMP Shield project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (pmp_shield/config/settings/common.py - 3 = pmp_shield/)
APPS_DIR = ROOT_DIR.path('pmp_shield')

TEST_OUTPUT_PATH = ROOT_DIR.path('output').root

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'auditlog',
    'acp_calendar',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'pmp_shield.users.apps.UsersConfig',
    'pmp_shield.employees',
    'pmp_shield.projects',
    'pmp_shield.risks',
    'pmp_shield.goals',
    # Your stuff: custom apps go here
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'pmp_shield.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Luis C. Berrocal""", 'luis.berrocal.1942@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres:///pmp_shield'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Panama'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap3_ad.auth.LDAP3ADBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = False  # True
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 'mandatory'

ACCOUNT_ADAPTER = 'pmp_shield.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'pmp_shield.users.adapters.SocialAccountAdapter'
ACCOUNT_ALLOW_REGISTRATION = False  # env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'login'

# SLUGLIFIER

#AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

########## CELERY
INSTALLED_APPS += ('pmp_shield.taskapp.celery.CeleryConfig',)
# if you are not using the django database broker (e.g. rabbitmq, redis, memcached), you can remove the next line.
INSTALLED_APPS += ('kombu.transport.django',)
BROKER_URL = env('CELERY_BROKER_URL', default='django://')
########## END CELERY



# Location of root django.contrib.admin URL, use  {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings

#  ##############################################
#     django_auth_ldap3_ad module configuration
#  ##############################################



LDAP_SERVERS = [
    {
        'host': env('LDAP_HOST'),
        'port': 389,
        'use_ssl': False,
    },
]
LDAP_USERNAME = env('LDAP_USERNAME')
LDAP_BIND_USER = r"<< %s LDAP_BIND_TEMPLATE>>" % LDAP_USERNAME
LDAP_BIND_PWD = env('LDAP_BIND_PWD')

LDAP_SEARCH_BASE = env('LDAP_SEARCH_BASE', default="ou=Corp,dc=canal,dc=acp")
LDAP_USER_SEARCH_FILTER = env('LDAP_USER_SEARCH_FILTER', default="(&(cn=%s)(objectClass=user))")
LDAP_USER_OBJECT_CLASS=env('LDAP_USER_OBJECT_CLASS', default="user")
LDAP_ATTRIBUTES_MAP = {
}

LDAP_USE_LDAP_GROUPS = False
LDAP_GROUPS_SEARCH_BASE = "dc=domain,dc=local"
LDAP_GROUPS_SEARCH_FILTER = "(&(objectClass=group))"
LDAP_GROUP_MEMBER_ATTRIBUTE = "member"
LDAP_SUPERUSER_GROUPS = ["CN=admin,dc=domain,dc=local", ]
LDAP_STAFF_GROUPS = ["CN=staff,dc=domain,dc=local", ]
LDAP_GROUPS_MAP = {
    'my django group': "cn=my ldap group,dc=domain,dc=local",
}


#  ##############################################
#  END django_auth_ldap3_ad module configuration
#  ##############################################
########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'cpc_admin_report.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'pmp_shield.users': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION

HR_PHOTO_URL = 'http://10.1.92.213:18134/ords/vtmsapi/employee/%s/photo/'
