from django import forms


class PlayForm(forms.Form):
    command = forms.CharField()
