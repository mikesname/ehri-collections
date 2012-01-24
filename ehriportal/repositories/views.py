"""Views for repositories."""

from django.views.generic import ListView
from django.shortcuts import render


from ehriportal.repositories.models import Repository


class RepoListView(ListView):
    """View class for Repository lists."""
    model = Repository
    template_name = "repositories/list.html"
    paginate_by = 20

