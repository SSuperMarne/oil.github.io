from django import forms
from .models import Tariff

class AddSurfForm(forms.Form):
    title = forms.CharField(max_length=120)
    url = forms.URLField()
    tariff = forms.ModelChoiceField(queryset=Tariff.objects.all(), empty_label=None)

class EditSurfForm(forms.Form):
    title = forms.CharField(max_length=120)
    url = forms.URLField()
    balance = forms.IntegerField()
    tariff = forms.ModelChoiceField(queryset=Tariff.objects.all(), empty_label=None)
    status = forms.BooleanField(required=False)