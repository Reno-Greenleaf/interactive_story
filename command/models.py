"""Command models."""
from django.db import models

from event.models import Event
from game.models import Game
from place.models import Place


class Command(models.Model):
    """Players action."""

    text = models.CharField(max_length=300, blank=False, null=False)
    success = models.TextField(default='')
    destination = models.ForeignKey(
        Place,
        null=True,
        on_delete=models.SET_NULL,
    )
    context = models.ForeignKey(
        Place,
        null=True,
        on_delete=models.SET_NULL,
        related_name='commands',
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='commands',
    )
    triggers = models.ForeignKey(
        Event,
        null=True,
        on_delete=models.SET_NULL,
        related_name='commands',
    )
    once = models.BooleanField(default=False)

    def __str__(self):
        """Mainly for editor.

        Returns:
            string
        """
        if self.context:
            return '{0} ({1})'.format(self.text, self.context.name)

        return self.text

    def execute(self, session):
        """Execute a command specified by player.

        Args:
            session: Session instance

        Returns:
            text about results of execution
        """
        events = session.happened.all()
        requirement = self.requirements.exclude(event__in=events).first()

        if requirement:
            output = requirement.fail
        elif self.once and self in session.executed.all():
            output = 'You did it already.'
        else:
            session.happened.add(self.triggers)
            session.executed.add(self)
            output = self.success

            if self.destination:
                session.place = self.destination
                session.save()

        return output


class Requirement(models.Model):
    """Condition under which a command succeeds."""

    class Meta:
        ordering = ('-priority',)

    command = models.ForeignKey(
        Command,
        on_delete=models.CASCADE,
        related_name='requirements',
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fail = models.TextField(default='')
    priority = models.PositiveSmallIntegerField(default=0)
