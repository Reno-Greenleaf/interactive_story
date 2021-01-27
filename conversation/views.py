from django.shortcuts import render
from game.views import GameView
from conversation.forms import ExchangeForm, OptionFormSet
from django.http import HttpResponseRedirect
from django.urls import reverse


class AddExchange(GameView):
    def get(self, request):
        form = ExchangeForm(self.current_game)
        conversations = self.current_game.conversations.filter(parent__isnull=True).all()
        options = OptionFormSet()
        return render(request, 'conversation/add-exchange.html', {'form': form, 'conversations': conversations, 'options': options})

    def post(self, request):
        form = ExchangeForm(self.current_game, request.POST)

        if not form.is_valid():
            conversations = self.current_game.conversations.filter(parent__isnull=True).all()
            return render(request, 'conversation/add-exchange.html', {'form': form, 'conversations': conversations})

        exchange = form.save(commit=False)
        exchange.game = self.current_game
        exchange.save()

        options = OptionFormSet(request.POST, instance=exchange)

        if options.is_valid():
            exchanges = options.save(commit=False)

            for exchange in exchanges:
                exchange.game = self.current_game
                exchange.save()
        else:
            return render(
                request,
                'conversation/add-exchange.html',
                {
                    'form': form,
                    'options': options,
                    'global_commands': self.current_game.conversations.filter(parent__isnull=True).all(),
                },
            )

        return HttpResponseRedirect(reverse('add-exchange'))
