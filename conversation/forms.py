from django import forms
from conversation.models import Exchange


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        exclude = ()
