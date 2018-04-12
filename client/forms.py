from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
STATUS_CHOICES = (
    (1, ("Payeer")),
    (2, ("QIWI")),
    (3, ("WebMoney"))
)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Пожалуйста, укажите верный E-mail адрес.')
    captcha = ReCaptchaField()
    ref = forms.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', )

class LPasswordForm(PasswordResetForm):
    captcha = ReCaptchaField()

class TransferForm(forms.Form):
    rubs = forms.IntegerField(min_value=1)
    system = forms.ChoiceField(choices = STATUS_CHOICES)
    vault = forms.CharField(min_length=5, max_length=64)

class AvatarForm(forms.Form):
    avatar = forms.ImageField()