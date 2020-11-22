from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from game.views import GameView
from event.models import Event
from event.forms import EventsForm


class Events(GameView):
    http_method_names = ['get', 'post']

    def get(self, request):
        events = self.current_game.events.order_by('chronology').all()
        names = []

        for event in events:
            names.append(event.name)

        context = {
            'form': EventsForm(initial={'events': '\n'.join(names)})
        }
        return render(request, 'event/events.html', context)

    def post(self, request):
        line_number = 1
        form = EventsForm(request.POST)

        if not form.is_valid():
            return render(request, 'event/events.html', {'form': form})

        lines = form.cleaned_data['events']

        for line in lines:
            event, created = self.current_game.events.get_or_create(name=line)
            event.chronology = line_number
            event.save()

            if created:
                messages.add_message(request, messages.INFO, 'Added "{0}"'.format(line))

            line_number += 1

        to_delete = self.current_game.events.exclude(name__in=lines)

        for event in to_delete:
            event.delete()
            messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(event.name))

        return HttpResponseRedirect(reverse('events'))
