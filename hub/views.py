from django.shortcuts import render
from django.views import View
from game.models import Game


class Main(View):
    """Starting point."""
    def get(self, request):
        return render(request, 'hub/main.html')
