from django import forms
from django.core.validators import RegexValidator
import re

def input_widget():
    return forms.TextInput(attrs={"class": "input-large"})

class JoinForm(forms.Form):
    username    = forms.CharField(max_length=100,
                                  widget=input_widget(),
                                  validators=[RegexValidator(regex      = re.compile("^[A-Za-z0-9]{3,}$"),
                                                             message    = "Should contain 3 or more letters A-Z or numbers 0-9 Should contain 3 or more ",
                                                             code       = "format")])
    
    
        
    