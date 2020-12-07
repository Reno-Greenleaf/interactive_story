"""Place form(s)."""
from django import forms


class PlaceForm(forms.Form):
    """Form to edit a place."""

    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)
