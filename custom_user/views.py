from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from custom_user.forms import LoginForm


class UserView(View):
    """Most views are meant for authenticated user."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.add_message(request, messages.INFO, 'You need to be authenticated to do it.')
        return HttpResponseRedirect(reverse('login'))


class Login(View):
    def get(self, request):
        return render(request, 'custom_user/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'custom_user/login.html', {'form': form})

        username = form.cleaned_data['name']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('games'))

        messages.add_message(request, messages.INFO, 'Credentials are invalid')
        return render(request, 'custom_user/login.html', {'form': form})


class Logout(UserView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('games'))
