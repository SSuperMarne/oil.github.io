from django import forms
STATUS_CHOICES = (
    (1, ("Payeer")),
    (2, ("QIWI")),
    (3, ("WebMoney"))
)

class ExchangeForm(forms.Form):
    rubs = forms.IntegerField(min_value=1)

class ReplenishForm(forms.Form):
    m_amount = forms.IntegerField(min_value=1)
    m_desc = forms.CharField(min_length=25, max_length=100)

class TransferForm(forms.Form):
    rubs = forms.IntegerField(min_value=1)
    system = forms.ChoiceField(choices = STATUS_CHOICES)
    vault = forms.CharField(min_length=5, max_length=64)