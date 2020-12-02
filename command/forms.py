"""Forms for commands."""
from django import forms

from command.models import Command, Requirement
from event.models import Event
from place.models import Place


class CommandForm(forms.Form):
    text = forms.CharField()
    success = forms.CharField(widget=forms.Textarea)
    context = forms.ModelChoiceField(
        Place.objects.none(),
        empty_label='<Any>',
        required=False,
    )
    destination = forms.ModelChoiceField(
        Place.objects.none(),
        empty_label='<Same>',
        required=False,
    )
    triggers = forms.ModelChoiceField(
        Event.objects.none(),
        empty_label='<Nothing>',
        required=False,
    )

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].queryset = game.places.all()
        self.fields['destination'].queryset = game.places.all()
        self.fields['triggers'].queryset = game.events.all()


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        exclude = ()

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = game.events.all()


RequirementsFormSet = forms.inlineformset_factory(Command, Requirement, exclude=(), extra=1, form=RequirementForm)
