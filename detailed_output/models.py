"""
Detailed output is a replacement of usual text field.

It provides more flexible piece of info for a player.
"""
from django.db import models

from event.models import Event


class DetailedOutput(models.Model):
    """Detailed output model."""

    general = models.TextField(default='')


class Paragraph(models.Model):
    """Paragraph with output depending on an event."""

    output = models.ForeignKey(
        DetailedOutput,
        on_delete=models.CASCADE,
        related_name='paragraphs',
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    before = models.TextField(default='')
    after = models.TextField(default='')
