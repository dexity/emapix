from django import forms
from django.core.validators import RegexValidator, validate_email, validate_slug
import re

from emapix.utils.const import *

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
    email       = forms.EmailField(max_length=100,
                                  widget=text_widget())
    password    = forms.CharField(max_length=30,
                                  widget=password_widget(),
                                  # XXX: Change password regex
                                  validators=[RegexValidator(regex      = re.compile("^[A-Za-z0-9]{6,30}$"),
                                                             message    = "Should contain from 6 to 30 letters A-Z or numbers 0-9",
                                                             code       = "password")])
    
    #location    = forms.CharField(max_length=100,
    #                              required=False,
    #                              widget=forms.TextInput(attrs={"class": "input-large",
    #                                                            "placeholder": "City, State"}))
    #country     = forms.ChoiceField(choices=[("", "Select Country")] + COUNTRY_CHOICES,
    #                                widget=forms.Select(attrs={"class": "input-medium"}))
    #
    #b_day       = forms.ChoiceField(choices=[("", "Day")],
    #                                widget=forms.Select(attrs={"class": "input-mini"}))
    #b_month     = forms.ChoiceField(choices=[("", "Month")] + MONTH_CHOICES,
    #                                widget=forms.Select(attrs={"class": "input-small"}))
    #b_year      = forms.ChoiceField(choices=[("", "Year")] + YEAR_CHOICES,
    #                                widget=forms.Select(attrs={"class": "input-mini"}),
    #                                validators=[validate_slug],
    #                                error_messages={'invalid': 'Enter the birth year.',
    #                                                'required': 'Birth year is required'})
    #gender      = forms.ChoiceField(choices=GENDER_CHOICES,
    #                                widget=forms.RadioSelect(),
    #                                initial='n')



    