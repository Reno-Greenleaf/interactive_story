from django.shortcuts import render
from django.views import View
from command.models import Command
from game.forms import PlayForm, GameForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from game.models import Game


class Player(View):
    def get(self, request):
        output = 'Unclear.'
        form = PlayForm(request.GET)
        command_text = request.GET.get('command', '')
        command = Command.objects.filter(text=command_text).first()

        if command:
            output = command.output

        return render(request, 'game/player.html', {'form': form, 'output': output})


class CreateGame(View):
    def get(self, request):
        games = Game.objects.all()
        form = GameForm()
        return render(request, 'game/create-game.html', {'form': form, 'games': games})

    def post(self, request):
        form = GameForm(request.POST)

        if not form.is_valid():
            games = Game.objects.all()
            return render(request, 'game/create-game.html', {'form': form, 'games': games})

        Game.objects.create(name=form.cleaned_data['name'])
        return HttpResponseRedirect(reverse('create-game'))


class EditGame(View):
    def get(self, request, game_id):
        games = Game.objects.all()
        game = Game.objects.get(pk=game_id)
        form = GameForm(initial={'name': game.name})
        return render(request, 'game/edit-game.html', {'games': games, 'game': game, 'form': form})

    def post(self, request, game_id):
        form = GameForm(request.POST)
        game = Game.objects.get(pk=game_id)

        if not form.is_valid():
            games = Games.objects.all()
            return render(request, 'game/edit-game.html', {'games': games, 'game': game, 'form': form})

        game.name = form.cleaned_data['name']
        game.save()
        return HttpResponseRedirect(reverse('create-game'))


class DeleteGame(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        return render(request, 'game/delete-game.html', {'game': game})

    def post(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        game.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(game.name))
        return HttpResponseRedirect(reverse('create-game'))
