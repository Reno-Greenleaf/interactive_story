"""Forms for commands."""
from django import forms

from command.models import Command, Requirement
from event.models import Event
from place.models import Place


class CommandForm(forms.Form):
    """Form to edit/add commands."""

    text = forms.CharField()
    success = forms.CharField(widget=forms.Textarea, required=False)
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
    once = forms.BooleanField(required=False)

    def __init__(self, game, *args, **kwargs):
        """Render selects based on current game.

        Args:
            game: Game model instance
            *args: default arguments of the form
            **kwargs: default keyword arguments of the form
        """
        super().__init__(*args, **kwargs)
        self.fields['context'].queryset = game.places.all()
        self.fields['destination'].queryset = game.places.all()
        self.fields['triggers'].queryset = game.events.all()


class RequirementForm(forms.ModelForm):
    """A case when a command fails."""

    class Meta(object):
        """Additional settings."""

        model = Requirement
        exclude = ()

    def __init__(self, game, *args, **kwargs):
        """Render selects based on current game.

        Args:
            game: Game model instance
            *args: default arguments of the form
            **kwargs: default keyword arguments of the form
        """
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = game.events.all()

    def has_changed(self):
        """Marely reordering a form doesn't mean it should be saved."""
        ignore = not self.instance.pk and not self['event'].value() and not self['fail'].value()

        if ignore:
            return False

        return super().has_changed()


RequirementsFormSet = forms.inlineformset_factory(
    Command,
    Requirement,
    exclude=(),
    extra=1,
    form=RequirementForm,
)
