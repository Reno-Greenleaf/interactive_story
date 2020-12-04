"""Event form(s)."""
from django import forms

from event.models import Event
from game.models import Game

EventsFormSet = forms.inlineformset_factory(Game, Event, exclude=(), extra=10)
