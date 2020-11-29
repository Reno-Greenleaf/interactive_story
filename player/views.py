from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from game.views import GameView
from game.models import Game
from player.forms import PlayForm
from player.models import Session


class Play(GameView):
    def get(self, request):
        session = Session.objects.get(pk=request.session['session_id'])

        output = 'Unclear.'
        form = PlayForm(request.GET)
        command_text = request.GET.get('command', '')
        place = session.game.starting_place
        command = session.game.commands.filter(text=command_text).first()

        if command:
            output = 'Requirements: '

            for requirement in command.requirements.all():
                output += ' ' + requirement.fail

            output += ' Success: ' + command.success

        return render(request, 'player/player.html', {'form': form, 'output': output, 'place': place, 'session': session})


class Start(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        session = game.sessions.create()
        request.session['session_id'] = session.pk
        return HttpResponseRedirect(reverse('play'))


class Continue(View):
    def get(self, request, session_id):
        request.session['session_id'] = session_id
        return HttpResponseRedirect(reverse('play'))
