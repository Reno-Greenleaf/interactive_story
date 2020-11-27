from django import forms
from place.models import Place
from event.models import Event


class CommandForm(forms.Form):
    text = forms.CharField()
    requirement = forms.ModelChoiceField(Event.objects.none(), empty_label='<None>', required=False)
    output = forms.CharField(widget=forms.Textarea)
    context = forms.ModelChoiceField(Place.objects.none(), empty_label='<Any>', required=False)
    destination = forms.ModelChoiceField(Place.objects.none(), empty_label='<Stay here>', required=False)

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].queryset = game.places.all()
        self.fields['destination'].queryset = game.places.all()
        self.fields['requirement'].queryset = game.events.all()
