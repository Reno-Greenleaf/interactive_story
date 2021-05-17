from django.contrib.auth.models import AbstractUser
from django.db import models


class Game(models.Model):
    """Interactive story itself."""
    title = models.CharField(max_length=256)
    public = models.BooleanField(default=False)


class User(AbstractUser):
    """Allows extending default user model."""
