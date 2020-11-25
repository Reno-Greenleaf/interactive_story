from django.db import models
from game.models import Game
from place.models import Place


class Command(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    output = models.TextField(default='')
    context = models.ForeignKey(Place, null=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='commands')
