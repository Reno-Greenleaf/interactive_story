from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=256)
    starting_place = models.ForeignKey('place.Place', on_delete=models.CASCADE, related_name='games', null=True)

    def __str__(self):
        return self.name
