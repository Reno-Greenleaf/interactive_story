"""Main hub views."""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from hub.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

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


class Authenticate(View):
    """Logs in a user."""

    def get(self, request):
        return render(request, 'hub/authenticate.html')

    def post(self, request):
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('start'))


class Logout(View):
    """Log out."""

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return HttpResponseRedirect(reverse('start'))


class Register(View):
    """Register a user."""

    def get(self, request):
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'hub/register.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authenticate'))

        context = {
            'form': form,
        }
        return render(request, 'hub/register.html', context)
