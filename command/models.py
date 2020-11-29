from django.db import models
from game.models import Game
from event.models import Event
from place.models import Place


class Command(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    success = models.TextField(default='')
    destination = models.ForeignKey(Place, null=True, on_delete=models.CASCADE)
    context = models.ForeignKey(Place, null=True, on_delete=models.CASCADE, related_name='commands')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='commands')

    def __str__(self):
        if self.context:
            return '{0} ({1})'.format(self.text, self.context.name)
        else:
            return self.text


class Requirement(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='requirements')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fail = models.TextField(default='')
