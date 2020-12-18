from django.db import models
from django.conf import settings


class Game(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=256)
    starting_place = models.ForeignKey('place.Place', on_delete=models.SET_NULL, related_name='games', null=True)

    def __str__(self):
        return self.name
