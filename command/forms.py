from django import forms
from place.models import Place


class CommandForm(forms.Form):
    text = forms.CharField()
    output = forms.CharField(widget=forms.Textarea)
    context = forms.ModelChoiceField(Place.objects.none(), empty_label='<Any>', required=False)

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].queryset = game.places.all()
