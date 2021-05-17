from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=256)
    public = models.BooleanField(default=False)
