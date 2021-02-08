"""Place form(s)."""
from django import forms
from place.models import Place


class PlaceForm(forms.ModelForm):
    """Form to edit a place."""

    class Meta:
        model = Place
        exclude = ('game', 'description')
