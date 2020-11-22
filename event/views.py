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
        events = Event.objects.order_by('chronology').all()
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
            event, created = Event.objects.get_or_create(name=line)
            event.chronology = line_number
            event.save()

            if created:
                messages.add_message(request, messages.INFO, 'Added "{0}"'.format(line))

            line_number += 1

        to_delete = Event.objects.exclude(name__in=lines)

        for event in to_delete:
            event.delete()
            messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(event.name))

        return HttpResponseRedirect(reverse('events'))
