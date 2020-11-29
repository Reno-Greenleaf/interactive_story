from django.db import models
from game.models import Game
from place.models import Place


class Session(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    started = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Started {0}'.format(self.started)
