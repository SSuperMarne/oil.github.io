from django import forms

class ReplenishForm(forms.Form):
    m_amount = forms.IntegerField(min_value=1)
    m_desc = forms.CharField(min_length=25, max_length=100)