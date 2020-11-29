from django.shortcuts import render
from django.views import View
from game.views import GameView
from player.forms import PlayForm
from player.models import Session


class Play(GameView):
    def get(self, request):
        if 'session_id' in request.session:
            session = self.current_game.sessions.get(pk=request.session['session_id'])
        else:
            session = self.current_game.sessions.create()
            request.session['session_id'] = session.pk

        output = 'Unclear.'
        form = PlayForm(request.GET)
        command_text = request.GET.get('command', '')
        place = self.current_game.starting_place
        command = self.current_game.commands.filter(text=command_text).first()

        if command:
            output = 'Requirements: '

            for requirement in command.requirements.all():
                output += ' ' + requirement.fail

            output += ' Success: ' + command.success

        return render(request, 'player/player.html', {'form': form, 'output': output, 'place': place, 'session': session})
