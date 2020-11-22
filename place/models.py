from django.db import models
from game.models import Game


class Place(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(default='')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='places')
