from django.template import Library
from emapix.utils import imageproc

register = Library()

@register.simple_tag
def image_serving_url(img):
    return imageproc.image_serving_url(img)