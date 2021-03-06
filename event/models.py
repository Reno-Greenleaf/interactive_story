"""Storage for events and related models."""
from django.db import models

from game.models import Game


class Event(models.Model):
    """Something that happens in a plot."""

    name = models.CharField(max_length=255)
    # it's convinient to view events in chronological order,
    # though it's not really meant to be used much.
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='events',
    )
    chronology = models.PositiveSmallIntegerField(default=0)

    class Meta(object):
        """Additional settings."""

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'game'],
                name='unique_event',
            ),
        ]
        ordering = ('chronology',)

    def __str__(self):
        """Event representation.

        Returns:
            string
        """
        return self.name
