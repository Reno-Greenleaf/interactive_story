from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from game.views import GameView
from game.models import Game
from command.models import Command
from command.forms import CommandForm, RequirementsFormSet


class AddCommand(GameView):
    def get(self, request):
        commands = self.current_game.commands.all()
        form = CommandForm(self.current_game)
        requirements = RequirementsFormSet(form_kwargs={'game': self.current_game})
        return render(request, 'command/add-command.html', {'commands': commands, 'form': form, 'requirements': requirements})

    def post(self, request):
        form = CommandForm(self.current_game, request.POST)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(request, 'command/add-command.html', {'commands': commands, 'form': form})

        command = self.current_game.commands.create(
            text=form.cleaned_data['text'],
            success=form.cleaned_data['success'],
            context = form.cleaned_data['context'],
            destination = form.cleaned_data['destination'],
            triggers = form.cleaned_data['triggers'],
        )

        requirements = RequirementsFormSet(request.POST, instance=command, form_kwargs={'game': self.current_game})

        if requirements.is_valid():
            requirements.save()

        return HttpResponseRedirect(reverse('add-command'))


class EditCommand(GameView):
    def get(self, request, command_id):
        commands = self.current_game.commands.all()
        command = self.current_game.commands.get(pk=command_id)
        requirements = RequirementsFormSet(instance=command, form_kwargs={'game': self.current_game})
        initial = {'text': command.text, 'success': command.success, 'context': command.context, 'destination': command.destination, 'triggers': command.triggers}
        form = CommandForm(self.current_game, initial=initial)
        return render(request, 'command/edit-command.html', {'commands': commands, 'command': command, 'form': form, 'requirements': requirements})

    def post(self, request, command_id):
        form = CommandForm(self.current_game, request.POST)
        command = self.current_game.commands.get(pk=command_id)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(request, 'command/edit-command.html', {'commands': commands, 'command': command, 'form': form})

        command.text = form.cleaned_data['text']
        command.success = form.cleaned_data['success']
        command.context = form.cleaned_data['context']
        command.destination = form.cleaned_data['destination']
        command.triggers = form.cleaned_data['triggers']
        command.save()

        requirements = RequirementsFormSet(request.POST, instance=command, form_kwargs={'game': self.current_game})

        if requirements.is_valid():
            requirements.save()

        return HttpResponseRedirect(reverse('edit-command', kwargs={'command_id': command.pk}))


class DeleteCommand(GameView):
    def get(self, request, command_id):
        command = self.current_game.commands.get(pk=command_id)
        return render(request, 'command/delete-command.html', {'command': command})

    def post(self, request, command_id):
        command = self.current_game.commands.get(pk=command_id)
        command.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(command.text))
        return HttpResponseRedirect(reverse('add-command'))
