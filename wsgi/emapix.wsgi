import os, sys
import django.core.handlers.wsgi as django_wsgi

path = '%s/..' % os.path.realpath(os.path.dirname(__file__))

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'emapix.settings'

application = django_wsgi.WSGIHandler()