from django import forms

from place.models import Place


class GameForm(forms.Form):
    name = forms.CharField()
    starting_place = forms.ModelChoiceField(
        queryset=Place.objects.none(),
        required=False,
        empty_label='<Anywhere>',
    )

    def __init__(self, game=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if game:
            self.fields['starting_place'].queryset = game.places.all()
