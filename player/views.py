from django.shortcuts import render
from game.views import GameView
from player.forms import PlayForm


class Play(GameView):
    def get(self, request):
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

        return render(request, 'player/player.html', {'form': form, 'output': output, 'place': place})
