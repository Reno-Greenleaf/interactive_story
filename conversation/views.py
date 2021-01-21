from django.shortcuts import render
from game.views import GameView
from conversation.forms import ExchangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class AddExchange(GameView):
    def get(self, request):
        form = ExchangeForm(self.current_game)
        conversations = self.current_game.conversations.filter(parent__isnull=True).all()
        return render(request, 'conversation/add-exchange.html', {'form': form, 'conversations': conversations})

    def post(self, request):
        form = ExchangeForm(self.current_game, request.POST)

        if not form.is_valid():
            conversations = self.current_game.conversations.filter(parent__isnull=True).all()
            return render(request, 'conversation/add-exchange.html', {'form': form, 'conversations': conversations})

        exchange = form.save(commit=False)
        exchange.game = self.current_game
        exchange.save()

        return HttpResponseRedirect(reverse('add-exchange'))
