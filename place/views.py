"""Views for places."""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from game.views import GameView
from place.forms import PlaceForm
from detailed_output.forms import DetailedOutputForm, ParagraphFormSet


class AddPlace(GameView):
    def get(self, request):
        form = PlaceForm()
        description = DetailedOutputForm()
        paragraphs = ParagraphFormSet(form_kwargs={'game': self.current_game})
        return self._render(request, form, description, paragraphs)

    def post(self, request):
        form = PlaceForm(request.POST)
        description_form = DetailedOutputForm(request.POST)
        paragraphs_form = ParagraphFormSet(
            request.POST,
            form_kwargs={'game': self.current_game},
        )

        if not form.is_valid() or not description_form.is_valid() or not paragraphs_form.is_valid():
            return self._render(request, form, description_form, paragraphs_form)

        detailed_output = description_form.save()
        paragraphs_form.instance = detailed_output
        paragraphs_form.save()

        place = form.save(commit=False)
        place.description = detailed_output
        place.game = self.current_game
        place.save()

        return HttpResponseRedirect(
            reverse('edit-place', kwargs={'place_id': place.pk}),
        )

    def _render(self, request, form, description, paragraphs):
        places = self.current_game.places.all()
        return render(
            request,
            'place/add-place.html',
            {
                'form': form,
                'description': description,
                'paragraphs': paragraphs,
                'places': places,
            },
        )


class EditPlace(GameView):
    def get(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        form = PlaceForm(instance=place)
        description = DetailedOutputForm(instance=place.description)
        paragraphs = ParagraphFormSet(instance=place.description)
        return self._render(request, form, description, paragraphs)

    def post(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        form = PlaceForm(request.POST)

        if not form.is_valid():
            places = self.current_game.places.all()
            return render(
                request,
                'place/edit-place.html',
                {'places': places, 'place': place, 'form': form},
            )

        place.name = form.cleaned_data['name']
        place.description = form.cleaned_data['description']
        place.save()
        return HttpResponseRedirect(
            reverse('edit-place', kwargs={'place_id': place.pk}),
        )

    def _render(self, request, form, description, paragraphs):
        places = self.current_game.places.all()
        return render(
            request,
            'place/edit-place.html',
            {
                'form': form,
                'description': description,
                'paragraphs': paragraphs,
                'places': places,
            },
        )


class DeletePlace(GameView):
    def get(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        return render(request, 'place/delete-place.html', {'place': place})

    def post(self, request, place_id):
        place = self.current_game.places.get(pk=place_id)
        place.delete()
        messages.add_message(
            request,
            messages.INFO,
            'Removed "{0}"'.format(place.name),
        )
        return HttpResponseRedirect(reverse('add-place'))
