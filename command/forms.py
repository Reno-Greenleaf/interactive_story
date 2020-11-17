from django import forms


class CommandForm(forms.Form):
    text = forms.CharField()
    output = forms.CharField(widget=forms.Textarea)
