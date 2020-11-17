from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from command.models import Command
from command.forms import CommandForm


class AddCommand(View):
    def get(self, request):
        commands = Command.objects.all()
        form = CommandForm()
        return render(request, 'command/add-command.html', {'commands': commands, 'form': form})

    def post(self, request):
        form = CommandForm(request.POST)

        if not form.is_valid():
            commands = Command.objects.all()
            return render(request, 'command/add-command.html', {'commands': commands, 'form': form})

        Command.objects.create(text=form.cleaned_data['text'], output=form.cleaned_data['output'])
        return HttpResponseRedirect(reverse('add-command'))


class EditCommand(View):
    def get(self, request, command_id):
        commands = Command.objects.all()
        command = Command.objects.get(pk=command_id)
        form = CommandForm(initial={'text': command.text, 'output': command.output})
        return render(request, 'command/edit-command.html', {'commands': commands, 'command': command, 'form': form})

    def post(self, request, command_id):
        form = CommandForm(request.POST)
        command = Command.objects.get(pk=command_id)

        if not form.is_valid():
            commands = Command.objects.all()
            return render(request, 'command/add-command.html', {'commands': commands, 'command': command, 'form': form})

        command.text = form.cleaned_data['text']
        command.output = form.cleaned_data['output']
        command.save()
        return HttpResponseRedirect(reverse('add-command'))


class DeleteCommand(View):
    def get(self, request, command_id):
        command = Command.objects.get(pk=command_id)
        return render(request, 'command/delete-command.html', {'command': command})

    def post(self, request, command_id):
        command = Command.objects.get(pk=command_id)
        command.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(command.text))
        return HttpResponseRedirect(reverse('add-command'))
