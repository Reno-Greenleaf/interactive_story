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

    def __init__(self, game, *args, **kwargs):
        """Render selects based on current game.

        Args:
            game: Game model instance
            *args: default arguments of the form
            **kwargs: default keyword arguments of the form
        """
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = game.events.all()


ParagraphFormSet = forms.inlineformset_factory(
    DetailedOutput,
    Paragraph,
    extra=2,
    form=ParagraphForm,
)
