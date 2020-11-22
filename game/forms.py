from django import forms


class PlayForm(forms.Form):
    command = forms.CharField()


class GameForm(forms.Form):
    name = forms.CharField()
