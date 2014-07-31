# Django settings for emapix project.

import os
from google.appengine.api import app_identity

try:
    # Available only for AppEngine environment
    APP_ID = app_identity.get_application_id()
    APP_MAILHOST = '{}.appspotmail.com'.format(APP_ID)
    APP_HOST = app_identity.get_default_version_hostname()
except AttributeError:
    APP_ID = None
    APP_MAILHOST = ''
    APP_HOST = ''
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

# Email
NOREPLY_EMAIL = 'noreply@{}'.format(APP_MAILHOST)
SENDGRID_USERNAME = ''
SENDGRID_PASSWORD = ''

ADMINS = (
    ('Alex Dementsov', 'dexity@gmail.com'),
)

S3_KEY = ''
S3_SECRET = ''
BUCKET_NAME = ''
API_KEY = ''  # test key for api
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

MANAGERS = ADMINS

DATABASES = {}

TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^!$%$usxu_e$a-6gllcuc_uv9i4&-nk#+-pl-o59c&js#31($n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'emapix.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'emapix.api',
    'emapix.prototype',
    'emapix.core',
    'emapix',
    'south',
    'constance',
    'constance.backends.database'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'emapix.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'constance.context_processors.config',
    'django.contrib.messages.context_processors.messages',
    'constance.context_processors.config'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
     },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'map_key': ('', 'Google Map key'),
    'google_analytics': ('', 'Google Analytics Tracking')
}

try:
    from local_settings import *
except ImportError:
    pass
