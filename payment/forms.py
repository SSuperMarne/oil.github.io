from django import forms
STATUS_CHOICES = (
    (1, ("FreeKassa")),
    (2, ("Payeer"))
)

class ReplenishForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    desc = forms.CharField(min_length=25, max_length=100)
    system = forms.ChoiceField(choices = STATUS_CHOICES)