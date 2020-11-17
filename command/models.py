from django.db import models


class Command(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    output = models.TextField(default='')
