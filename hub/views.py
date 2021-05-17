"""Main hub views."""
from django.shortcuts import render
from django.views import View

from hub.models import Game


class Main(View):
    """Starting point."""

    def get(self, request):
        return render(request, 'hub/main.html')


class List(View):
    """List games."""

    def get(self, request):
        context = {
            'games': Game.objects.filter(public=True).all(),
        }
        return render(request, 'hub/list.html', context)
