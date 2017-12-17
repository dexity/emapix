
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from recaptcha.client import captcha


class ReCaptcha(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def render(self, name, value, attrs=None):
        s = '<input type="text" id="recaptcha_response_field" name="recaptcha_response_field" class="form-control"/>'
        s += u'%s' % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)
        return mark_safe(s)

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None),
                data.get(self.recaptcha_response_name, None)]
