from django.db import models
from game.models import Game


class Command(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    output = models.TextField(default='')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='commands')
