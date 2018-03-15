from django import forms

class ModForm(forms.Form):
    nickname = forms.CharField(max_length=150)
    oil = forms.IntegerField()
    rub = forms.IntegerField()