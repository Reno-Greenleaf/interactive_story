"""Views for commands."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from command.forms import CommandForm, RequirementsFormSet
from game.views import GameView

GAME_KEY = 'game'
COMMANDS_KEY = 'commands'
FORM_KEY = 'form'


class AddCommand(GameView):
    """Add new command."""

    def get(self, request):
        """Render command form.

        Args:
            request: HttpRequest instance

        Returns:
            HttpResponse
        """
        commands = self.current_game.commands.all()
        form = CommandForm(self.current_game)
        requirements = RequirementsFormSet(
            form_kwargs={GAME_KEY: self.current_game},
        )
        return render(
            request,
            'command/add-command.html',
            {
                COMMANDS_KEY: commands,
                FORM_KEY: form,
                'requirements': requirements,
            },
        )

    def post(self, request):
        """Create a command.

        Args:
            request: HttpRequest instance

        Returns:
            HttpResponseRedirect
        """
        form = CommandForm(self.current_game, request.POST)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(
                request,
                'command/add-command.html',
                {COMMANDS_KEY: commands, FORM_KEY: form},
            )

        command = self.current_game.commands.create(
            text=form.cleaned_data['text'],
            success=form.cleaned_data['success'],
            context=form.cleaned_data['context'],
            destination=form.cleaned_data['destination'],
            triggers=form.cleaned_data['triggers'],
        )

        requirements = RequirementsFormSet(
            request.POST,
            instance=command,
            form_kwargs={GAME_KEY: self.current_game},
        )

        if requirements.is_valid():
            requirements.save()

        return HttpResponseRedirect(reverse('add-command'))


class EditCommand(GameView):
    """Edit existing command."""

    def get(self, request, command_id):
        """Render edit form.

        Args:
            request: HttpRequest instance
            command_id: integer

        Returns:
            HttpResponse
        """
        commands = self.current_game.commands.all()
        command = self.current_game.commands.get(pk=command_id)
        requirements = RequirementsFormSet(
            instance=command,
            form_kwargs={GAME_KEY: self.current_game},
        )
        initial = {
            'text': command.text,
            'success': command.success,
            'context': command.context,
            'destination': command.destination,
            'triggers': command.triggers,
        }
        form = CommandForm(self.current_game, initial=initial)
        return render(
            request,
            'command/edit-command.html',
            {
                COMMANDS_KEY: commands,
                'command': command,
                FORM_KEY: form,
                'requirements': requirements,
            },
        )

    def post(self, request, command_id):
        """Edit command.

        Args:
            request: HttpRequest instance
            command_id: integer

        Returns:
            HttpResponseRedirect
        """
        form = CommandForm(self.current_game, request.POST)
        command = self.current_game.commands.get(pk=command_id)

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(
                request,
                'command/edit-command.html',
                {COMMANDS_KEY: commands, 'command': command, FORM_KEY: form},
            )

        command.text = form.cleaned_data['text']
        command.success = form.cleaned_data['success']
        command.context = form.cleaned_data['context']
        command.destination = form.cleaned_data['destination']
        command.triggers = form.cleaned_data['triggers']
        command.save()

        requirements = RequirementsFormSet(
            request.POST,
            instance=command,
            form_kwargs={GAME_KEY: self.current_game},
        )

        if requirements.is_valid():
            requirements.save()

        return HttpResponseRedirect(
            reverse('edit-command', kwargs={'command_id': command.pk}),
        )


class DeleteCommand(GameView):
    """Delete a command."""

    def get(self, request, command_id):
        """Show confirmation form.

        Args:
            request: HttpRequest instance
            command_id: integer

        Returns:
            HttpResponse
        """
        command = self.current_game.commands.get(pk=command_id)
        return render(
            request,
            'command/delete-command.html',
            {'command': command},
        )

    def post(self, request, command_id):
        """Do delete.

        Args:
            request: HttpRequest instance
            command_id: integer

        Returns:
            HttpResponseRedirect instance
        """
        command = self.current_game.commands.get(pk=command_id)
        command.delete()
        messages.add_message(
            request,
            messages.INFO,
            'Removed "{0}"'.format(command.text),
        )
        return HttpResponseRedirect(reverse('add-command'))
