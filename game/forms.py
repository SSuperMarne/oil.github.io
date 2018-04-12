from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class ExchangeForm(forms.Form):
    rubs = forms.IntegerField(min_value=1)