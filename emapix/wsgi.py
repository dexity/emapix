import os
import sys
import django.core.handlers.wsgi as django_wsgi

sys.path.append("%s/../../" % os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, '../libs2')

os.environ["DJANGO_SETTINGS_MODULE"] = "emapix.settings"

application = django_wsgi.WSGIHandler()