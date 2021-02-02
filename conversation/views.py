"""Views to edit conversations."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from conversation.forms import ExchangeForm, OptionFormSet
from game.views import GameView


class AddExchange(GameView):
    """Add starting exchange for a conversation."""

    def get(self, request):
        form = ExchangeForm(self.current_game)
        conversations = self.current_game.exchanges.filter(parent__isnull=True).all()
        options = OptionFormSet()
        return render(
            request,
            'conversation/add-exchange.html',
            {'form': form, 'conversations': conversations, 'options': options},
        )

    def post(self, request):
        form = ExchangeForm(self.current_game, request.POST)
        options_form = OptionFormSet(request.POST)

        if not form.is_valid():
            conversations = self.current_game.exchanges.filter(parent__isnull=True).all()
            return render(
                request,
                'conversation/add-exchange.html',
                {'form': form, 'conversations': conversations},
            )

        exchange = form.save(commit=False)
        exchange.game = self.current_game
        exchange.save()

        options_form.instance = exchange

        if options_form.is_valid():
            options = options_form.save(commit=False)

            for option in options:
                option.game = self.current_game
                option.save()
        else:
            return render(
                request,
                'conversation/add-exchange.html',
                {
                    'form': form,
                    'options': options_form,
                    'conversations': self.current_game.exchanges.filter(parent__isnull=True).all(),
                },
            )

        return HttpResponseRedirect(reverse('edit-exchange', kwargs={'exchange_id': exchange.pk}))


class EditExchange(GameView):
    """Edit exchange page."""

    def get(self, request, exchange_id):
        exchange = self.current_game.exchanges.get(pk=exchange_id)
        form = ExchangeForm(self.current_game, instance=exchange)
        conversations = self.current_game.exchanges.filter(parent__isnull=True).all()
        options = OptionFormSet(instance=exchange)
        return render(request, 'conversation/edit-exchange.html', {'form': form, 'conversations': conversations, 'options': options})

    def post(self, request, exchange_id):
        exchange = self.current_game.exchanges.get(pk=exchange_id)
        form = ExchangeForm(self.current_game, request.POST, instance=exchange)
        options_form = OptionFormSet(request.POST, instance=exchange)

        if not form.is_valid():
            conversations = self.current_game.exchanges.filter(parent__isnull=True).all()
            return render(
                request,
                'conversation/edit-exchange.html',
                {'form': form, 'conversations': conversations},
            )

        exchange = form.save(commit=False)
        exchange.game = self.current_game
        exchange.save()

        if options_form.is_valid():
            options = options_form.save(commit=False)

            for option in options:
                option.game = self.current_game
                option.save()
        else:
            return render(
                request,
                'conversation/edit-exchange.html',
                {
                    'form': form,
                    'options': options_form,
                    'conversations': self.current_game.exchanges.filter(parent__isnull=True).all(),
                },
            )

        return HttpResponseRedirect(reverse(
            'edit-exchange',
            kwargs={'exchange_id': exchange.pk},
        ))


class DeleteExchange(GameView):
    """Delete exchange page."""

    def get(self, request, exchange_id):
        exchange = self.current_game.exchanges.get(pk=exchange_id)
        return render(
            request,
            'conversation/delete-exchange.html',
            {'exchange': exchange},
        )

    def post(self, request, exchange_id):
        exchange = self.current_game.exchanges.get(pk=exchange_id)
        exchange.delete()
        messages.add_message(
            request,
            messages.INFO,
            'Exchange "{0}" is removed.'.format(exchange.option),
        )
        return HttpResponseRedirect(reverse('add-exchange'))
