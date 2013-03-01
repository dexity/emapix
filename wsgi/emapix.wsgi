import os, sys
import django.core.handlers.wsgi as django_wsgi

sys.path.append("/etc/emapix")
sys.path.append("%s/.." % os.path.realpath(os.path.dirname(__file__)))

os.environ["DJANGO_SETTINGS_MODULE"] = "emapix.settings"

application = django_wsgi.WSGIHandler()