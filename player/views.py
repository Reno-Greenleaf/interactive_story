"""Player views."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from custom_user.views import UserView
from game.models import Game
from player.forms import PlayForm
from player.models import Session


class Play(UserView):
    """Run current session."""

    def get(self, request):
        session = Session.objects.get(pk=request.session['session_id'])

        output = 'Unclear.'
        command_text = request.GET.get('command', '')
        command = session.place.commands.filter(text=command_text).first()

        if command:
            output = command.execute(session)

        context = {
            'form': PlayForm(),
            'output': output,
            'session': session,
        }

        return render(request, 'player/player.html', context)


class Start(UserView):
    """Start new play session."""

    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)

        if not game.starting_place:
            messages.add_message(
                request,
                messages.INFO,
                "There's no place to start.",
            )
            return HttpResponseRedirect(reverse('games'))

        session = game.sessions.create(place=game.starting_place)
        request.session['session_id'] = session.pk
        return HttpResponseRedirect(reverse('play'))


class Continue(UserView):
    """Continue existing play session."""

    def get(self, request, session_id):
        request.session['session_id'] = session_id
        return HttpResponseRedirect(reverse('play'))
