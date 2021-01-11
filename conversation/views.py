from django.shortcuts import render
from game.views import GameView
from conversation.forms import ExchangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class AddExchange(GameView):
    def get(self, request):
        form = ExchangeForm()
        return render(request, 'conversation/add-exchange.html', {'form': form})

    def post(self, request):
        form = ExchangeForm(request.POST)

        if not form.is_valid():
            return render(request, 'conversation/add-exchange.html', {'form': form})

        exchange = form.save(commit=False)
        exchange.game = self.current_game
        exchange.save()

        return HttpResponseRedirect(reverse('games'))
