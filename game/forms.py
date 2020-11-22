from django import forms
from game.models import Game


class PlayForm(forms.Form):
    command = forms.CharField()


class GameForm(forms.Form):
    name = forms.CharField()


class SelectGameForm(forms.Form):
    games = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        empty_label='<Select a game>',
    )
