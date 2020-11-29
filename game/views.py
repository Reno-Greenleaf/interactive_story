from django.shortcuts import render
from django.views import View
from command.models import Command
from game.forms import GameForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from game.models import Game


class GameView(View):
    def dispatch(self, request, *args, **kwargs):
        game_id = request.session.get('game', 0)

        try:
            self.current_game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            messages.add_message(request, messages.INFO, "A game isn't selected.")
            return HttpResponseRedirect(reverse('games'))

        return super().dispatch(request, *args, **kwargs)


class CreateGame(View):
    def get(self, request):
        games = Game.objects.all()
        form = GameForm(None)
        return render(request, 'game/create-game.html', {'form': form, 'games': games})

    def post(self, request):
        form = GameForm(None, request.POST)

        if not form.is_valid():
            games = Game.objects.all()
            return render(request, 'game/create-game.html', {'form': form, 'games': games})

        game = Game.objects.create(name=form.cleaned_data['name'])
        request.session['game'] = game.pk
        messages.add_message(request, messages.INFO, 'Selected {0}'.format(game.name))
        return HttpResponseRedirect(reverse('events'))


class EditGame(GameView):
    def get(self, request):
        games = Game.objects.all()
        game = self.current_game
        form = GameForm(self.current_game, initial={'name': game.name, 'starting_place': game.starting_place})
        return render(request, 'game/edit-game.html', {'games': games, 'game': game, 'form': form})

    def post(self, request):
        form = GameForm(self.current_game, request.POST)
        game = self.current_game

        if not form.is_valid():
            games = Games.objects.all()
            return render(request, 'game/edit-game.html', {'games': games, 'game': game, 'form': form})

        game.name = form.cleaned_data['name']
        game.starting_place = form.cleaned_data['starting_place']
        game.save()
        return HttpResponseRedirect(reverse('events'))


class DeleteGame(GameView):
    def get(self, request):
        return render(request, 'game/delete-game.html', {'game': self.current_game})

    def post(self, request):
        game = self.current_game
        game.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(game.name))
        request.session['game'] = 0
        return HttpResponseRedirect(reverse('games'))


class SelectGame(View):
    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        request.session['game'] = game.pk
        messages.add_message(request, messages.INFO, 'Selected {0}'.format(game.name))
        return HttpResponseRedirect(reverse('events'))


class Games(View):
    def get(self, request):
        games = Game.objects.all()
        return render(request, 'game/games.html', {'games': games})
