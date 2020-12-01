"""Event form(s)."""
from django import forms
from django.core.exceptions import ValidationError


class Multiline(forms.CharField):
    """Form field for multiple values."""

    widget = forms.Textarea

    def to_python(self, value):
        """Clean up input.

        Args:
            value: multiline text

        Returns:
            list
        """
        converted = []

        for line in value.split('\n'):
            line = line.strip()

            if line != '':
                converted.append(line)

        return converted

    def validate(self, value):
        """Validate event names."""
        super().validate(value)
        checked = set()
        errors = set()

        for line in value:
            if line in checked:
                errors.add('{0} is not unique'.format(line))
            else:
                checked.add(line)

        if errors:
            raise ValidationError(list(errors))


class EventsForm(forms.Form):
    """Form to edit plot as a whole."""

    events = Multiline(
        help_text='Outline the plot by listing unique events.',
        required=False,
    )
