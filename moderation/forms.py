from django import forms

class ModifyForm(forms.Form):
    nickname = forms.CharField(max_length=150)
    oil = forms.IntegerField()
    rub = forms.IntegerField()

class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=150)