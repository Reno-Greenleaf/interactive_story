from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from game.views import GameView
from game.models import Game
from command.models import Command
from command.forms import CommandForm


class AddCommand(GameView):
    def get(self, request):
        commands = self.current_game.commands.all()
        form = CommandForm()
        return render(request, 'command/add-command.html', {'commands': commands, 'form': form})

    def post(self, request):
        form = CommandForm(request.POST)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(request, 'command/add-command.html', {'commands': commands, 'form': form})

        self.current_game.commands.create(text=form.cleaned_data['text'], output=form.cleaned_data['output'])
        return HttpResponseRedirect(reverse('add-command'))


class EditCommand(GameView):
    def get(self, request, command_id):
        commands = self.current_game.commands.all()
        command = self.current_game.commands.get(pk=command_id)
        form = CommandForm(initial={'text': command.text, 'output': command.output})
        return render(request, 'command/edit-command.html', {'commands': commands, 'command': command, 'form': form})

    def post(self, request, command_id):
        form = CommandForm(request.POST)
        command = self.current_game.commands.get(pk=command_id)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(request, 'command/edit-command.html', {'commands': commands, 'command': command, 'form': form})

        command.text = form.cleaned_data['text']
        command.output = form.cleaned_data['output']
        command.save()
        return HttpResponseRedirect(reverse('add-command'))


class DeleteCommand(GameView):
    def get(self, request, command_id):
        command = self.current_game.commands.get(pk=command_id)
        return render(request, 'command/delete-command.html', {'command': command})

    def post(self, request, command_id):
        command = self.current_game.commands.get(pk=command_id)
        command.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(command.text))
        return HttpResponseRedirect(reverse('add-command'))
