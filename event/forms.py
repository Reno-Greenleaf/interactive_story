"""Event form(s)."""
from django import forms

from event.models import Event
from game.models import Game


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()

    def has_changed(self):
        """Marely reordering a form doesn't mean it should be saved."""
        ignore = not self.instance.pk and not self['name'].value()

        if ignore:
            return False

        return super().has_changed()


EventsFormSet = forms.inlineformset_factory(Game, Event, form=EventForm, extra=10)
