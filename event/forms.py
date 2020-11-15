from django import forms
from django.core.exceptions import ValidationError


class Multiline(forms.CharField):
    widget = forms.Textarea

    def to_python(self, value):
        converted = []

        for line in value.split('\n'):
            line = line.strip()

            if line != '':
                converted.append(line)

        return converted

    def validate(self, value):
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
    events = Multiline(help_text='Outline the plot by listing unique events.')
