from django.template import Library
from emapix.utils.utils import template_str

register = Library()


@register.simple_tag
def jstmpl(value):
    return template_str(value)
