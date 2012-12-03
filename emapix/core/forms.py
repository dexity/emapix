
import re
from django import forms
from django.core.validators import RegexValidator, validate_email, validate_slug
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from emapix.core.validators import *
from emapix.utils.const import *
from emapix.core.fields import ReCaptchaField

from emapix.utils.logger import Logger
logger = Logger.get("emapix.core.forms")

def text_widget():
    return forms.TextInput(attrs={"class": "input-large"})

def password_widget():
    return forms.PasswordInput(attrs={"class": "input-large"})

def hidden_field():
    return forms.CharField(widget=forms.HiddenInput())


class JoinForm(forms.Form):
    username    = forms.CharField(max_length=100,
                                  widget=text_widget(),
                                  validators=[RegexValidator(regex      = re.compile(USERNAME_REGEX),
                                                             message    = "Should contain 5 or more letters A-Z or numbers 0-9",
                                                             code       = "username"),
                                              UsernameExists("Username already exists",
                                                            "username_exists",
                                                            User.objects)])
    email       = forms.EmailField(max_length=100,
                                  widget=text_widget(),
                                  validators=[EmailExists("Email already exists",
                                                           "email_exists",
                                                           User.objects)])
    password    = forms.CharField(max_length=30,
                                  widget=password_widget(),
                                  validators=[RegexValidator(regex      = re.compile(PASSWORD_REGEX),
                                                             message    = "Should contain from 6 to 30 letters A-Z or numbers 0-9",
                                                             code       = "password")])
    location    = forms.CharField(max_length=100,
                                  required=False,
                                  widget=forms.TextInput(attrs={"class": "input-large",
                                                                "placeholder": "City, State"}))
    country     = forms.ChoiceField(choices=[("", "Select Country")] + COUNTRY_CHOICES,
                                    required=False,
                                    widget=forms.Select(attrs={"class": "input-medium"}))
    
    b_day       = forms.ChoiceField(choices=[("", "Day")],
                                    required=False,
                                    widget=forms.Select(attrs={"class": "input-mini"}))
    b_month     = forms.ChoiceField(choices=[("", "Month")] + MONTH_CHOICES,
                                    required=False,
                                    widget=forms.Select(attrs={"class": "input-small"}))
    b_year      = forms.ChoiceField(choices=[("", "Year")] + YEAR_CHOICES,
                                    widget=forms.Select(attrs={"class": "input-mini"}),
                                    validators=[validate_slug],
                                    error_messages={'invalid': 'Enter the birth year.',
                                                    'required': 'Birth year is required'})
    gender      = forms.ChoiceField(choices=GENDER_CHOICES,
                                    widget=forms.RadioSelect(),
                                    initial='n')


class RecaptchaForm(forms.Form):
    recaptcha   = ReCaptchaField()
    

class LoginForm(forms.Form):
    username    = forms.CharField(max_length=100,
                                  widget=text_widget(),
                                  validators=[RegexValidator(regex      = re.compile(USERNAME_REGEX))])
    password    = forms.CharField(max_length=30,
                                  widget=password_widget(),
                                  validators=[RegexValidator(regex      = re.compile(PASSWORD_REGEX))])    

    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        username    = cleaned_data.get("username")
        password    = cleaned_data.get("password")
        
        msg     = "Username or password is not valid"
        code    = "auth_invalid"
        if username is None or password is None:   # one of them or both are invalid
            raise forms.ValidationError(msg, code=code)
            
        # Check if user entered right credentials
        user    = authenticate(username=username, password=password)
        if user is None:    # authentication failed
            raise forms.ValidationError(msg, code=code)
        
        if not user.is_active:
            raise forms.ValidationError("User profile is not activated. Please check email", code="activ_failed")
        
        cleaned_data["user"]    = user
        return cleaned_data
        
    
class ForgotForm(forms.Form):
    email       = forms.EmailField(max_length=100,
                                  widget=text_widget())
    
    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        email    = cleaned_data.get("email")        
    
        msg     = "Account with this email does not exist"
        code    = "email_invalid"
        if email is None:
            raise forms.ValidationError(msg, code=code)
        try:
            user    = User.objects.get(email=email)
            cleaned_data["user"]    = user
            return cleaned_data
        except Exception, e:
            raise forms.ValidationError(msg, code=code)


class NewPasswordForm(forms.Form):
    newpass    = forms.CharField(max_length=30,
                                  widget=password_widget(),
                                  validators=[RegexValidator(regex      = re.compile(PASSWORD_REGEX),
                                                             message    = "Should contain from 6 to 30 letters A-Z or numbers 0-9",
                                                             code       = "password")])
    renewpass  = forms.CharField(max_length=30,
                                  widget=password_widget())
    
    def clean(self):
        cleaned_data = super(forms.Form, self).clean()
        newpass     = cleaned_data.get("newpass")
        renewpass   = cleaned_data.get("renewpass")
        
        if newpass != renewpass:
            raise forms.ValidationError("Passwords do not match", code="passwords_match")
        
        return cleaned_data
    
    
class RequestForm(forms.Form):
    lat     = forms.FloatField(widget=forms.HiddenInput())
    lon     = forms.FloatField(widget=forms.HiddenInput())
    description = forms.CharField(min_length=6, max_length=140,
                                  error_messages={"min_length": "Should be at least 6 characters",
                                                  "max_length": "Should be less than 140 characters"},
                                  widget    = forms.Textarea(attrs={"rows": 3, "placeholder": "I want to see ..."}))
    
    #def clean(self):
    #    cleaned_data = super(forms.Form, self).clean()
    #    #lat, lon
    #
    #    return cleaned_data
    

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    

class CropForm(forms.Form):
    x   = forms.FloatField(widget=forms.HiddenInput())
    y   = forms.FloatField(widget=forms.HiddenInput())
    h   = forms.FloatField(widget=forms.HiddenInput())
    w   = forms.FloatField(widget=forms.HiddenInput())
    

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=3072)
