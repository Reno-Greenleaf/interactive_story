from django import forms
from place.models import Place
from game.models import Game


class PlayForm(forms.Form):
    command = forms.CharField()


class GameForm(forms.Form):
    name = forms.CharField()
    starting_place = forms.ModelChoiceField(queryset=Place.objects.none(), required=False)

    def __init__(self, game = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if game:
            print(game)
            self.fields['starting_place'].queryset = game.places.all()
