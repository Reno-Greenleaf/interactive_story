from django import forms
from detailed_output.models import DetailedOutput, Paragraph


class DetailedOutputForm(forms.ModelForm):
    class Meta:
        model = DetailedOutput
        exclude = ()


class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        exclude = ()


ParagraphFormSet = forms.inlineformset_factory(
    DetailedOutput,
    Paragraph,
    extra=2,
    form=ParagraphForm,
)
