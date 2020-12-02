"""Place model."""
from django.db import models

from game.models import Game


class Place(models.Model):
    """Place for a player to travel to/from."""

    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(default='')
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='places',
    )

    def __str__(self):
        return self.name
