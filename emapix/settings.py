# Django settings for emapix project.

import os.path
from google.appengine.api import app_identity

try:
    import emapixconf
except:
    import emapixconf_default as emapixconf

APP_ID = app_identity.get_application_id()
APP_MAILHOST = "{}.appspotmail.com".format(APP_ID)
APP_HOST = app_identity.get_default_version_hostname()
DEBUG   = emapixconf.DEBUG
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

# Email
#NOREPLY_EMAIL  = "noreply@emapix.com"
NOREPLY_EMAIL = "noreply@{}".format(APP_MAILHOST)

if DEBUG:
    EMAIL_BACKEND   = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/emapix_emails'
else:
    EMAIL_BACKEND   = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST      = emapixconf.EMAIL_HOST
    EMAIL_PORT      = emapixconf.EMAIL_PORT
    EMAIL_HOST_USER = emapixconf.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = emapixconf.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS   = emapixconf.EMAIL_USE_TLS


ADMINS = emapixconf.ADMINS

S3_KEY      = emapixconf.S3_KEY
S3_SECRET   = emapixconf.S3_SECRET
BUCKET_NAME = emapixconf.BUCKET_NAME
API_KEY     = emapixconf.API_KEY    # test key for api

RECAPTCHA_PUBLIC_KEY    = emapixconf.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY   = emapixconf.RECAPTCHA_PRIVATE_KEY


MANAGERS    = ADMINS

DATABASES   = emapixconf.DATABASES

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^!$%$usxu_e$a-6gllcuc_uv9i4&-nk#+-pl-o59c&js#31($n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'emapix.middleware.access.AccessMiddleware',    # checks keys
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'emapix.urls'

TEMPLATE_DIRS = (
    #os.path.join(os.path.dirname(__file__), 'layout/templates'),
    os.path.join(os.path.dirname(__file__), 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
    'emapix.layout',
    'emapix.core',
    'emapix',
    'south',
    'constance',
    'constance.backends.database'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "emapix.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "constance.context_processors.config",
    "django.contrib.messages.context_processors.messages",
    "constance.context_processors.config"
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

CONSTANCE_BACKEND   = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG    = {
    "map_key": ("", "Google Map key"),
    "google_analytics": ("", "Google Analytics Tracking")
}
