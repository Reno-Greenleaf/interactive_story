"""Form(s) to edit conversations."""
from django import forms

from conversation.models import Exchange


class ExchangeForm(forms.ModelForm):
    """Form to edit exchange."""

    class Meta(object):
        """Exchange form settings."""

        model = Exchange
        exclude = ('game', 'parent', 'option')

    def __init__(self, game, *args, **kwargs):
        """Render selects based on current game.

        Args:
            game: Game model instance
            *args: default arguments of the form
            **kwargs: default keyword arguments of the form
        """
        super().__init__(*args, **kwargs)
        self.fields['triggers'].queryset = game.events.all()


OptionFormSet = forms.inlineformset_factory(
    Exchange,
    Exchange,
    extra=3,
    fields=('option',),
    can_delete=False,
)
