from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Пожалуйста, укажите верный E-mail адрес.')
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', )

class LPasswordForm(PasswordResetForm):
    captcha = ReCaptchaField()