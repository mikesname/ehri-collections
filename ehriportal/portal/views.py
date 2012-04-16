"""Portal search views."""

import re
import datetime
import json

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

from haystack.query import SearchQuerySet
from portal import models, forms, utils


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
        sqs = self.searchqueryset
        if self.model:
            sqs = sqs.models(self.model)
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
        # FIXME: Find out why spelling suggestions aren't handled properly
        extra["suggestion"] = re.sub("[\W-]", "", self.searchqueryset\
                    .spelling_suggestion() or "")
        extra["querystring"] = self.request.META.get("QUERY_STRING", "")
        return extra

    def render_to_response(self, context, **rkwargs):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            response = HttpResponse(mimetype="application/json")
            json.dump(context["page_obj"], response, cls=utils.HaystackPaginationEncoder)
            return response
        return super(PortalSearchListView, self).render_to_response(
                    context, **rkwargs)



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


def edit_collection(request, slug):
    """Edit a collection using a formset."""
    collection = get_object_or_404(models.Collection, slug=slug)
    form = forms.CollectionEditForm(instance=collection)
    dates = forms.DateFormSet(instance=collection)
    othernames = forms.OtherNameFormSet(instance=collection)

    properties = ["language", "script", "language_of_description", 
            "script_of_description"]
    propforms = {}
    for propname in properties:
        propforms[propname] = forms.propertyformset_factory(models.Collection,
                propname)(instance=collection, prefix=propname)

    if request.method == "POST":
        form = forms.CollectionEditForm(
                request.POST, request.FILES, instance=collection)
        dates = forms.DateFormSet(
                request.POST, request.FILES, instance=collection)
        othernames = forms.OtherNameFormSet(
                request.POST, request.FILES, instance=collection)
        for propname in properties:
            propforms[propname] = forms.propertyformset_factory(models.Collection,
                    propname)(request.POST, request.FILES, instance=collection, prefix=propname)
        if form.is_valid() and dates.is_valid() and othernames.is_valid() \
                and False not in [pf.is_valid() for pf in propforms.values()]:
            form.save()
            dates.save()
            othernames.save()
            [pf.save() for pf in propforms.values()]
            return HttpResponseRedirect(collection.get_absolute_url())
    context = dict(form=form, dates=dates, othernames=othernames,
            propforms=propforms)
    template = "collection_form.html"
    return render(request, template, context)
