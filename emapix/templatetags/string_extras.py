from django.template.defaultfilters import stringfilter
from HTMLParser import HTMLParser

from django.template import Library

register = Library()

@stringfilter
def html_decode(value):
    p   = HTMLParser()
    return p.unescape(value)

register.filter('html_decode', html_decode)