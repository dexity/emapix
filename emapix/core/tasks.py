import logging
from django import http
from django import shortcuts
from django.contrib.auth import models as auth_models
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from emapix.core import models as emapix_models
from emapix.core.db.image import WImage
from emapix.utils.imageproc import load_s3image, proc_image
from emapix.utils.utils import storage_filename


@csrf_exempt
@require_POST
def crop_image_task(*args, **kwargs):
    return http.HttpResponse()


@csrf_exempt
@require_POST
def process_image_task(request, res, *args, **kwargs):
    """Processes image in queue task."""
    data = request.POST
    req = shortcuts.get_object_or_404(emapix_models.Request, resource=res)
    user = shortcuts.get_object_or_404(auth_models.User, username=data['username'])
    file_base = res
    fmt = data['format']
    size = data['size']
    size_type = data['size_type']

    img = load_s3image(res, fmt)  # Temp image

    im  = WImage.get_or_create_image_by_request(user, req, "request", size_type)
    im.name = storage_filename(file_base, size_type, fmt)
    im.save()
    proc_image(size, im, file_base, img.copy(), fmt)
    return http.HttpResponse()
