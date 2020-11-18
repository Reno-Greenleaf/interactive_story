from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(default='')
