from django.db import models
from game.models import Game
from event.models import Event
from place.models import Place


class Command(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    output = models.TextField(default='')
    destination = models.ForeignKey(Place, null=True, on_delete=models.CASCADE)
    context = models.ForeignKey(Place, null=True, on_delete=models.CASCADE, related_name='commands')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='commands')
    requirement = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='commands')
