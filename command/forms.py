from django import forms
from place.models import Place
from event.models import Event
from command.models import Command, Requirement


class CommandForm(forms.Form):
    text = forms.CharField()
    success = forms.CharField(widget=forms.Textarea)
    context = forms.ModelChoiceField(Place.objects.none(), empty_label='<Any>', required=False)
    destination = forms.ModelChoiceField(Place.objects.none(), empty_label='<Same>', required=False)

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].queryset = game.places.all()
        self.fields['destination'].queryset = game.places.all()


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        exclude = ()

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = game.events.all()


RequirementsFormSet = forms.inlineformset_factory(Command, Requirement, exclude=(), extra=1, form=RequirementForm)
