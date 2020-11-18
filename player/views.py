from django.shortcuts import render
from django.views import View
from command.models import Command
from player.forms import PlayForm


class Player(View):
    def get(self, request):
        output = 'Unclear.'
        form = PlayForm(request.GET)
        command_text = request.GET.get('command', '')
        command = Command.objects.filter(text=command_text).first()

        if command:
            output = command.output

        return render(request, 'player/player.html', {'form': form, 'output': output})
