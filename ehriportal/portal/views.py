# Create your views here.

import re
import datetime

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django import forms
from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse

from haystack.query import SearchQuerySet

from portal import models, forms


class PortalSearchListView(ListView):
    """A view which performs a search using Haystack and parses
    the facet information into a form that is easily manageable
    for display within the template."""
    model = None
    searchqueryset = None
    paginate_by = 20
    facetclasses = []
    form_class = forms.PortalSearchForm

    def get_queryset(self):
        """Perform the appropriate Haystack search and return
        a SearchQuerySet with the obtained results."""
        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()
        sqs = self.searchqueryset.models(self.model)
        for facet in self.facetclasses:
            sqs = facet.apply(sqs)

        # apply the query
        self.form = self.form_class(self.request.GET)
        if self.form.is_valid():
            sqs = self.form.filter(sqs)
        for facetclass in self.facetclasses:
            sqs = facetclass.narrow(sqs, self.request.GET.getlist(
                facetclass.paramname))
        counts = sqs.facet_counts()
        current = sqs.query.narrow_queries
        for facetclass in self.facetclasses:
            facetclass.parse(counts, current)

        self.searchqueryset = sqs
        return self.searchqueryset

    def get_context_data(self, *args, **kwargs):
        extra = super(PortalSearchListView, self).get_context_data(*args, **kwargs)
        extra["facet_classes"] = self.facetclasses
        extra["form"] = self.form
        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False) and \
                self.form.is_valid():
            extra["suggestion"] = self.searchqueryset\
                    .spelling_suggestion(self.form.cleaned_data['q'])
        extra["querystring"] = self.request.META.get("QUERY_STRING", "")
        return extra


class PaginatedFacetView(PortalSearchListView):
    """Subclass of the standard facet view which displays
    a paginated list of items for a given facet (whose name
    is passed in the URL) so that the user can select one."""
    paginate_by = 10
    template_name = "facets.html"
    template_name_ajax = "facets_ajax.html"
    redirect = None
    
    def __init__(self, *args, **kwargs):
        super(PaginatedFacetView, self).__init__(*args, **kwargs)
        self.fclass = None

    def get_queryset(self):
        sqs = super(PaginatedFacetView, self).get_queryset()
        # look for the active facet
        counts = self.searchqueryset.facet_counts()
        current = self.searchqueryset.query.narrow_queries
        try:
           self.fclass = [fc for fc in self.facetclasses \
                    if fc.name == self.kwargs["facet"]][0]
        except IndexError:
            raise Http404
        self.fclass.parse(counts, current)
        if self.form.cleaned_data["sort"] == "count":
            return self.fclass.sorted_by_count()
        return self.fclass.sorted_by_name()

    def get_template_names(self, **kwargs):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        extra = super(PaginatedFacetView, self).get_context_data(**kwargs)
        extra["facetclass"] = self.fclass
        # FIXME: This is probably a bit fragile since we're assuming
        # we redirect to a path like /collections/search
        extra["redirect"] = self.request.get_full_path()
        if self.redirect:
            extra["redirect"] = "%s?%s" % (reverse(self.redirect),
                    self.request.META.get("QUERY_STRING",""))
        return extra

