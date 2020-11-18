from django import forms


class PlaceForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
