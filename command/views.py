"""Views for commands."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from command.forms import CommandForm, RequirementsFormSet
from game.views import GameView


class AddCommand(GameView):
    """Add new command."""

    def get(self, request):
        """Render command form.

        Args:
            request: HttpRequest instance

        Returns:
            HttpResponse
        """
        global_commands = self.current_game.commands.filter(context=None).all()
        form = CommandForm(self.current_game)
        requirements = RequirementsFormSet(
            form_kwargs={'game': self.current_game},
        )
        return render(
            request,
            'command/add-command.html',
            {
                'form': form,
                'requirements': requirements,
                'global_commands': global_commands,
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
        requirements = RequirementsFormSet(
            request.POST,
            form_kwargs={'game': self.current_game},
        )

        if not form.is_valid():
            commands = self.current_game.commands.order_by('context').all()
            return render(
                request,
                'command/add-command.html',
                {'commands': commands, 'form': form},
            )

        command = form.save(commit=False)
        command.game = self.current_game
        command.save()

        requirements.instance = command

        if requirements.is_valid():
            requirements.save()
        else:
            return render(
                request,
                'command/add-command.html',
                {
                    'form': form,
                    'requirements': requirements,
                    'global_commands': self.current_game.commands.filter(context=None).all(),
                },
            )

        return HttpResponseRedirect(
            reverse('edit-command', kwargs={'command_id': command.pk}),
        )


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
        global_commands = self.current_game.commands.filter(context=None).all()
        command = self.current_game.commands.get(pk=command_id)
        requirements = RequirementsFormSet(
            instance=command,
            form_kwargs={'game': self.current_game},
        )
        form = CommandForm(self.current_game, instance=command)
        return render(
            request,
            'command/edit-command.html',
            {
                'global_commands': global_commands,
                'command': command,
                'form': form,
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
        command = self.current_game.commands.get(pk=command_id)
        form = CommandForm(self.current_game, request.POST, instance=command)
        requirements = RequirementsFormSet(
            request.POST,
            instance=command,
            form_kwargs={'game': self.current_game},
        )

        if not form.is_valid():
            commands = self.current_game.commands.all()
            return render(
                request,
                'command/edit-command.html',
                {'commands': commands, 'command': command, 'form': form},
            )

        command = form.save(commit=False)
        command.game = self.current_game
        command.save()

        if requirements.is_valid():
            requirements.save()
        else:
            return render(
                request,
                'command/edit-command.html',
                {
                    'global_commands': self.current_game.commands.filter(context=None).all(),
                    'command': command,
                    'form': form,
                    'requirements': requirements,
                },
            )

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
