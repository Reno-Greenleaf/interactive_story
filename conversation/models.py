"""Models for conversations."""
from django.db import models

from event.models import Event
from game.models import Game


class Exchange(models.Model):
    """Element of a conversation."""

    parent = models.ForeignKey(
        'Exchange',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    option = models.CharField(max_length=512)
    output = models.TextField()
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='exchanges',
    )
    triggers = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def save(self):
        """Populate data from different forms for one model."""
        if not self.pk and not self.output:
            self.output = self.option

        super().save()
