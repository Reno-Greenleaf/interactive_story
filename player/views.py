"""Player views."""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from game.models import Game
from player.forms import PlayForm
from player.models import Session


class Play(View):
    """Run current session."""

    def get(self, request):
        session = Session.objects.get(pk=request.session['session_id'])

        output = 'Unclear.'
        form = PlayForm(request.GET)
        command_text = request.GET.get('command', '')
        place = session.game.starting_place
        command = session.game.commands.filter(text=command_text).first()

        if command:
            requirement = command.requirements.exclude(event__in=session.happened.all()).order_by('-priority').first()

            if requirement:
                output = requirement.fail
            else:
                session.happened.add(command.triggers)
                output = command.success

        context = {
            'form': form,
            'output': output,
            'place': place,
            'session': session,
        }

        return render(request, 'player/player.html', context)


class Start(View):
    """Start new play session."""

    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        session = game.sessions.create()
        request.session['session_id'] = session.pk
        return HttpResponseRedirect(reverse('play'))


class Continue(View):
    """Continue existing play session."""

    def get(self, request, session_id):
        request.session['session_id'] = session_id
        return HttpResponseRedirect(reverse('play'))
