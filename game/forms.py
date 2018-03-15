from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class SupportForm(forms.Form):
    title = forms.CharField(max_length=128)
    text = forms.CharField(max_length=2048)
    captcha = ReCaptchaField()