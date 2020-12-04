"""View(s) to edit events."""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from event.forms import EventsFormSet
from game.views import GameView


class Events(GameView):
    """Edit events form."""

    http_method_names = ['get', 'post']

    def get(self, request):
        formset = EventsFormSet(instance=self.current_game)

        context = {'formset': formset}
        return render(request, 'event/events.html', context)

    def post(self, request):
        formset = EventsFormSet(request.POST, instance=self.current_game)

        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('events'))

        return render(request, 'event/events.html', {'formset': formset})
