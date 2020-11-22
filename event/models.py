from django.db import models
from game.models import Game


class Event(models.Model):
    name = models.CharField(max_length=255)
    # it's convinient to view events in chronological order,
    # though it's not really meant to be used much.
    chronology = models.PositiveSmallIntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'game'], name='unique_event')
        ]
