from django import forms

class ExchangeForm(forms.Form):
    rubs = forms.IntegerField(min_value=1)

class ReplenishForm(forms.Form):
    m_amount = forms.IntegerField(min_value=1)
    m_desc = forms.CharField(min_length=25, max_length=100)