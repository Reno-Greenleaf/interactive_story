"""Form(s) for player."""
from django import forms


class PlayForm(forms.Form):
    """Main mean of interaction for a player."""

    command = forms.CharField()
