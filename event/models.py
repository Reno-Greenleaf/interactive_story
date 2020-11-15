from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # it's convinient to view events in chronological order,
    # though it's not really meant to be used much.
    chronology = models.PositiveSmallIntegerField(default=0)
