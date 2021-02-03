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
        form = CommandForm(self.current_game)
        requirements = RequirementsFormSet(
            form_kwargs={'game': self.current_game},
        )
        return self._render(request, form, requirements)

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
            return self._render(request, form, requirements)

        command = form.save(commit=False)
        command.game = self.current_game
        command.save()

        requirements.instance = command

        if requirements.is_valid():
            requirements.save()
        else:
            return self._render(request, form, requirements)

        return HttpResponseRedirect(
            reverse('edit-command', kwargs={'command_id': command.pk}),
        )

    def _render(self, request, form, requirements_form):
        global_commands = self.current_game.commands.filter(context=None).all()
        return render(
            request,
            'command/add-command.html',
            {
                'form': form,
                'requirements': requirements_form,
                'global_commands': global_commands,
            },
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
        command = self.current_game.commands.get(pk=command_id)
        requirements = RequirementsFormSet(
            instance=command,
            form_kwargs={'game': self.current_game},
        )
        form = CommandForm(self.current_game, instance=command)
        return self._render(request, form, requirements)

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
            return self._render(request, form, requirements)

        command = form.save(commit=False)
        command.game = self.current_game
        command.save()

        if requirements.is_valid():
            requirements.save()
        else:
            return self._render(request, form, requirements)

        return HttpResponseRedirect(
            reverse('edit-command', kwargs={'command_id': command.pk}),
        )

    def _render(self, request, form, requirements_form):
        global_commands = self.current_game.commands.filter(context=None).all()
        return render(
            request,
            'command/edit-command.html',
            {
                'global_commands': global_commands,
                'form': form,
                'requirements': requirements_form,
            },
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
