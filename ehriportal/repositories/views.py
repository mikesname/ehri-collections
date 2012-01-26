"""Views for repositories."""

from django.views.generic import ListView
from django.shortcuts import render


from ehriportal.repositories.models import Repository

from haystack.views import FacetedSearchView

class RepoListView(ListView):
    """View class for Repository lists."""
    model = Repository
    template_name = "repositories/list.html"
    paginate_by = 20


class CountFacetedSearchView(FacetedSearchView):
    """Include full (unqueried) facet counts in haystack's original context."""
    __name__ = 'CountFacetedSearchView'
    
    def extra_context(self):
        extra = super(CountFacetedSearchView, self).extra_context()
        extra['facet_counts'] = self.searchqueryset.facet_counts()
        # sort counts, ideally we'd do this in the template
        for facet in extra["facet_counts"]["fields"].keys():
            extra["facet_counts"]["fields"][facet].sort(
                    lambda x, y: cmp(x[0], y[0]))
        print extra
        return extra

