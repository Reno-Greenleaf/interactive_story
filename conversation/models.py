from django.db import models
from game.models import Game
from event.models import Event


class Exchange(models.Model):
    """Element of a conversation."""

    parent = models.ForeignKey('Exchange', on_delete=models.CASCADE, null=True, blank=True)
    option = models.CharField(max_length=512)
    output = models.TextField()
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='conversations',
    )
    triggers = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
