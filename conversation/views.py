from django.shortcuts import render
from game.views import GameView
from conversation.forms import ExchangeForm


class AddExchange(GameView):
    def get(self, request):
        form = ExchangeForm()
        return render(request, 'conversation/add-exchange.html', {'form': form})
