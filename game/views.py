"""Views for games."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from custom_user.views import UserView
from game.forms import GameForm
from game.models import Game


class GameView(UserView):
    """Base view for editor views."""

    def dispatch(self, request, *args, **kwargs):
        game_id = request.session.get('game', 0)

        try:
            self.current_game = request.user.games.get(pk=game_id)
        except Game.DoesNotExist:
            messages.add_message(
                request,
                messages.INFO,
                "A game isn't selected or you aren't its author.",
            )
            return HttpResponseRedirect(reverse('games'))

        return super().dispatch(request, *args, **kwargs)


class CreateGame(UserView):
    """Create new game."""

    def get(self, request):
        games = Game.objects.all()
        form = GameForm(None)
        return render(request, 'game/create-game.html', {'form': form, 'games': games})

    def post(self, request):
        form = GameForm(None, request.POST)

        if not form.is_valid():
            games = Game.objects.all()
            return render(request, 'game/create-game.html', {'form': form, 'games': games})

        game = Game.objects.create(
            name=form.cleaned_data['name'],
            author=request.user,
        )
        request.session['game'] = game.pk
        messages.add_message(
            request,
            messages.INFO,
            'Selected {0}'.format(game.name),
        )
        return HttpResponseRedirect(reverse('events'))


class EditGame(GameView):
    """Edit main game properties."""

    def get(self, request):
        games = Game.objects.all()
        game = self.current_game
        form = GameForm(
            self.current_game,
            initial={'name': game.name, 'starting_place': game.starting_place},
        )
        return render(
            request,
            'game/edit-game.html',
            {'games': games, 'game': game, 'form': form},
        )

    def post(self, request):
        form = GameForm(self.current_game, request.POST)
        game = self.current_game

        if not form.is_valid():
            games = Games.objects.all()
            return render(
                request,
                'game/edit-game.html',
                {'games': games, 'game': game, 'form': form},
            )

        game.name = form.cleaned_data['name']
        game.starting_place = form.cleaned_data['starting_place']
        game.save()
        return HttpResponseRedirect(reverse('events'))


class DeleteGame(GameView):
    """Delete a game and all its data."""

    def get(self, request):
        return render(
            request,
            'game/delete-game.html',
            {'game': self.current_game},
        )

    def post(self, request):
        game = self.current_game
        game.delete()
        messages.add_message(
            request,
            messages.INFO,
            'Removed "{0}"'.format(game.name),
        )
        request.session['game'] = 0
        return HttpResponseRedirect(reverse('games'))


class SelectGame(UserView):
    """Select game for editing."""

    def get(self, request, game_id):
        try:
            game = request.user.games.get(pk=game_id)
        except Game.DoesNotExist:
            messages.add_message(
                request,
                messages.INFO,
                "You aren't the author.",
            )
            return HttpResponseRedirect(reverse('games'))

        request.session['game'] = game.pk
        messages.add_message(
            request,
            messages.INFO,
            'Selected {0}'.format(game.name),
        )
        return HttpResponseRedirect(reverse('events'))


class Games(View):
    """List existing games (main page)."""

    def get(self, request):
        games = Game.objects.all()
        return render(request, 'game/games.html', {'games': games})
