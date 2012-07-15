from django import forms
from django.core.validators import RegexValidator, validate_email
import re

def text_widget():
    return forms.TextInput(attrs={"class": "input-large"})

def password_widget():
    return forms.PasswordInput(attrs={"class": "input-large"})

class JoinForm(forms.Form):
    username    = forms.CharField(max_length=100,
                                  widget=text_widget(),
                                  validators=[RegexValidator(regex      = re.compile("^[A-Za-z0-9]{5,}$"),
                                                             message    = "Should contain 5 or more letters A-Z or numbers 0-9",
                                                             code       = "username")])
    email       = forms.CharField(max_length=100,
                                  widget=text_widget(),
                                  validators=[validate_email],
                                  error_messages={'invalid': 'Enter a valid e-mail address.'})
    password    = forms.CharField(max_length=30,
                                  widget=password_widget(),
                                  # XXX: Change password regex
                                  validators=[RegexValidator(regex      = re.compile("^[A-Za-z0-9]{6,30}$"),
                                                             message    = "Should contain from 6 to 30 letters A-Z or numbers 0-9",
                                                             code       = "password")])
    #location
    #birthday
    #gender
    
        # required=False
    
        
    