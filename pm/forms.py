from django import forms
from captcha.fields import ReCaptchaField

class NewPMForm(forms.Form):
    username = forms.CharField(max_length=150)
    title = forms.CharField(max_length=120)
    text = forms.CharField(max_length=3000)
    captcha = ReCaptchaField()

class AddPMForm(forms.Form):
    text = forms.CharField(max_length=3000)
    captcha = ReCaptchaField()

class AddSupportForm(forms.Form):
    text = forms.CharField(max_length=3000)
    captcha = ReCaptchaField()

class ReplySupportForm(forms.Form):
    text = forms.CharField(max_length=3000)
    close = forms.BooleanField(required=False)