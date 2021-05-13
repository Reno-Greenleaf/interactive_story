from django.views.generic import TemplateView
from django.shortcuts import render


class Placeholder(TemplateView):
    """Use it before an actual view is created."""
    template_name = 'interactive_story/placeholder.txt'
