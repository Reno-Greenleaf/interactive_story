from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from game.views import GameView
from place.models import Place
from place.forms import PlaceForm


class AddPlace(GameView):
    def get(self, request):
        form = PlaceForm()
        places = self.current_game.places.all()
        return render(request, 'place/add-place.html', {'form': form, 'places': places})

    def post(self, request):
        form = PlaceForm(request.POST)

        if not form.is_valid():
            places = self.current_game.places.all()
            return render(request, 'place/add-place.html', {'form': form, 'places': places})

        self.current_game.places.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
        return HttpResponseRedirect(reverse('add-place'))


class EditPlace(GameView):
    def get(self, request, place_id):
        places = self.current_game.places.all()
        place = self.current_game.places.get(pk=place_id)
        form = PlaceForm(initial={'name': place.name, 'description': place.description})
        return render(request, 'place/edit-place.html', {'places': places, 'place': place, 'form': form})

    def post(self, request, place_id):
        form = PlaceForm(request.POST)
        place = self.current_game.places.get(pk=place_id)

        if not form.is_valid():
            places = self.current_game.places.all()
            return render(request, 'place/edit-place.html', {'places': places, 'place': place, 'form': form})

        place.name = form.cleaned_data['name']
        place.description = form.cleaned_data['description']
        place.save()
        return HttpResponseRedirect(reverse('add-place'))


class DeletePlace(GameView):
    def get(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        return render(request, 'place/delete-place.html', {'place': place})

    def post(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        place.delete()
        messages.add_message(request, messages.INFO, 'Removed "{0}"'.format(place.name))
        return HttpResponseRedirect(reverse('add-place'))
