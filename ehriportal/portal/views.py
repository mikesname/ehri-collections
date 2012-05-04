"""Portal search views."""

import re
import datetime
import json
import socket

from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, DeleteView, UpdateView, ProcessFormView
from django.views.generic.detail import DetailView
from django import forms
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render

from haystack.query import SearchQuerySet
from haystack.forms import EmptySearchQuerySet
from portal import models, forms, utils
import reversion


class PortalSearchListView(ListView, FormMixin):
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
        # check this for Solr connection errors.
        self.form = self.get_form(self.form_class)
        try:
            return self.get_searchqueryset(self.form)
        except socket.error:
            msg = _("We're terribly sorry but it looks like the search engine is "
                    "not working at the moment. We've been notified of this error "
                    "so please try again or check back soon.")
            messages.add_message(self.request, messages.ERROR, msg)
        return EmptySearchQuerySet()

    def get_form_kwargs(self):
        return dict(data=self.request.GET)

    def get_searchqueryset(self, form):
        """Get the Haystack searchqueryset (which we treat as
        a regular Django queryset."""
        sqs = SearchQuerySet()
        if self.model:
            sqs = sqs.models(self.model)
        # FIXME: Move somewhere more sensible
        if settings.PORTAL_HIDE_DRAFTS and not self.request.user.is_staff:
            sqs = sqs.narrow("publication_status:%d" % models.Resource.PUBLISHED)

        for facet in self.facetclasses:
            sqs = facet.apply(sqs)

        # apply the query
        if form.is_valid():
            sqs = form.filter(sqs)
        for facetclass in self.facetclasses:
            sqs = facetclass.narrow(sqs, self.request.GET.getlist(
                facetclass.paramname))
        counts = sqs.facet_counts()
        current = sqs.query.narrow_queries
        for facetclass in self.facetclasses:
            facetclass.parse(counts, current)

        # FIXME: Find way around assigning the sqs to the instance,
        # but it seems to be difficult to prevent it from running
        # multiple times otherwise, e.g. when checking for a spelling
        # suggestion.
        self.searchqueryset = sqs
        return sqs

    def get_context_data(self, *args, **kwargs):
        extra = super(PortalSearchListView, self).get_context_data(*args, **kwargs)
        extra["facet_classes"] = self.facetclasses
        extra["form"] = self.form

        # FIXME: This spelling suggestion stuff could be improved:
        # 1. it relies on the instance searchqueryset (which may not
        #    be re-entrant.)
        # 2. It uses a hacky method to extract the 'query' param from
        #    others that were applied with filter() (such as publication
        #    status). This assumes that the query (plain text) param is
        #    always last after any OR or AND clauses.
        if self.searchqueryset is not None:
            suggestion = self.searchqueryset.spelling_suggestion()
            if suggestion:
                qmatch = re.match(".*(?:(?:AND|OR) )?\((?P<query>[^\)]+)\)", suggestion)
                if qmatch:
                    extra["suggestion"] = qmatch.group("query")
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

    def get_searchqueryset(self, form):
        sqs = super(PaginatedFacetView, self).get_searchqueryset(form)
        # look for the active facet
        counts = sqs.facet_counts()
        current = sqs.query.narrow_queries
        try:
           self.fclass = [fc for fc in self.facetclasses \
                    if fc.name == self.kwargs["facet"]][0]
        except IndexError:
            raise Http404
        self.fclass.parse(counts, current)
        if form.cleaned_data["sort"] == "count":
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


class PortalListView(ListView):
    """Filter items depending on whether the user is
    logged in."""
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super(PortalListView, self).get_queryset(*args, **kwargs)
        if settings.PORTAL_HIDE_DRAFTS and not self.request.user.is_staff:
            qs = qs.filter(publication_status=models.Resource.PUBLISHED)
        return qs


class ListCollectionsView(PortalListView):
    """View which displays the collections for a particular 
    repository, and added that repository to the template
    context."""
    model = models.Collection
    related_item_attr = None
    related_item_model = None
    def get_queryset(self, *args, **kwargs):
        qs = super(ListCollectionsView, self).get_queryset(*args, **kwargs)
        if self.related_item_model is not None:
            self.item = get_object_or_404(
                    self.related_item_model, slug=self.kwargs["slug"])
        return qs.filter(**{self.related_item_attr: self.item})

    def get_context_data(self, *args, **kwargs):
        extra = super(ListCollectionsView, self).get_context_data(*args, **kwargs)
        if self.related_item_model is not None:
            extra[self.related_item_attr] = self.item
        return extra


# The Create and Edit actions for Repository, Collection, and Authority
# models are all pretty much the same, and based on the Django UpdateView
# generic template class. The only thing that varies is the specific
# formsets they use. What we do here is create a base class derived from
# update view that works pretty much the the `BookCreateView` detailed 
# here: http://haineault.com/blog/155/
#
# We just need to override the `get_formsets` method in each model-
# specific subclass to return a dictionary of formsets specific to
# each entity.

class PortalUpdateView(UpdateView):
    """Base class for entity create/edit that require
    formsets in addition to their main form."""
    def get_formsets(self):
        raise NotImplementedError

    def get_object(self):
        if self.kwargs.get("slug"):
            return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def form_valid(self, form):
        context = self.get_context_data()
        formsets = context["formsets"]
        if False not in [pf.is_valid() for pf in formsets.values()]:
            # run update in a reversion 
            with reversion.create_revision():
                reversion.set_user(self.request.user)
                comment = form.cleaned_data["revision_comment"].strip()
                if not comment:
                    comment = "Created" if not self.object else "Updated"
                reversion.set_comment(comment)
                self.object = form.save()
                for formset in formsets.values():
                    formset.instance = self.object
                    formset.save()
                return HttpResponseRedirect(self.object.get_absolute_url())
        return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PortalUpdateView, self).get_context_data(**kwargs)
        context["formsets"] = self.get_formsets()
        return context


class CollectionEditView(PortalUpdateView):
    """Generic form implementation for creating or updating a
    collection object."""
    form_class = forms.CollectionEditForm
    model = models.Collection
    template_name = "collection_form.html"

    def get_formsets(self):
        formsets = {}
        if self.request.method == "POST":
            formsets["dates"] = forms.DateFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
            formsets["othernames"] = forms.OtherNameFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
        else:
            formsets["dates"] = forms.DateFormSet(instance=self.object)
            formsets["othernames"] = forms.OtherNameFormSet(instance=self.object)
        return formsets

class RepositoryCollectionCreateView(CollectionEditView):
    """Specialisation of collection edit view for 
    creating a collection in the context of a
    particular repository."""
    def get_object(self):
        # this view only works for creating 
        # new collections
        return

    def get_initial(self, *args, **kwargs):
        initial = super(RepositoryCollectionCreateView, self)\
                .get_initial(*args, **kwargs)
        initial["repository"] = get_object_or_404(
                models.Repository, slug=self.kwargs["slug"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(RepositoryCollectionCreateView, self)\
                .get_context_data(**kwargs)
        return context


class CollectionDeleteView(DeleteView):
    template_name = "collection_confirm_delete.html"
    success_url = reverse_lazy("collection_search")
    model = models.Collection


class RepositoryEditView(PortalUpdateView):
    """Generic form implementation for creating or updating a
    repository object."""
    form_class = forms.RepositoryEditForm
    model = models.Repository
    template_name = "repository_form.html"

    def get_formsets(self):
        formsets = {}
        if self.request.method == "POST":
            formsets["contacts"] = forms.ContactFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
            formsets["parallelnames"] = forms.ParallelNameFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
            formsets["othernames"] = forms.OtherNameFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
        else:
            formsets["contacts"] = forms.ContactFormSet(instance=self.object)
            formsets["parallelnames"] = forms.ParallelNameFormSet(instance=self.object)
            formsets["othernames"] = forms.OtherNameFormSet(instance=self.object)
        return formsets


class RepositoryDeleteView(DeleteView):
    template_name = "repository_confirm_delete.html"
    success_url = reverse_lazy("repository_search")
    model = models.Repository


class PortalHistoryView(ListView):
    model = None
    template_name = "history_base.html"
    paginate_by = 5
    def get_queryset(self, *args, **kwargs):
        self.object = get_object_or_404(self.model, slug=self.kwargs["slug"])
        return reversion.get_for_object(self.object)

    def get_context_data(self, **kwargs):
        context = super(PortalHistoryView, self).get_context_data(**kwargs)
        context["object"] = self.object
        return context


class AuthorityEditView(PortalUpdateView):
    """Generic form implementation for creating or updating a
    authority object."""
    form_class = forms.AuthorityEditForm
    model = models.Authority
    template_name = "authority_form.html"

    def get_formsets(self):
        formsets = {}
        if self.request.method == "POST":
            formsets["othernames"] = forms.OtherNameFormSet(
                    self.request.POST, self.request.FILES, instance=self.object)
        else:
            formsets["othernames"] = forms.OtherNameFormSet(instance=self.object)
        return formsets


class AuthorityDeleteView(DeleteView):
    template_name = "authority_confirm_delete.html"
    success_url = reverse_lazy("authority_search")
    model = models.Authority


class PortalDetailView(DetailView):
    """Show information about an object."""
    def get_object(self, *args, **kwargs):
        """Enforce visibility constrains."""
        object = super(PortalDetailView, self).get_object(*args, **kwargs)
        # FIXME: Move this check somewhere nicer...
        if settings.PORTAL_HIDE_DRAFTS:
            if not self.request.user.is_staff \
                    and not object.published:
                # FIXME: Find a way to redirect to somewhere else
                raise PermissionDenied()
        return object

    def get_context_data(self, **kwargs):
        context = super(PortalDetailView, self).get_context_data(**kwargs)
        context["history"] = reversion.get_for_object(self.object)
        return context


class PortalCollectionHolderDetailView(PortalDetailView):
    """Add the number of viewable collections to the
    context."""
    def get_context_data(self, **kwargs):
        context = super(PortalCollectionHolderDetailView, self)\
                .get_context_data(**kwargs)
        
        viewcols = self.object.collection_set.all()
        if settings.PORTAL_HIDE_DRAFTS and not self.request.user.is_staff:
                viewcols = viewcols.filter(
                    publication_status=models.Resource.PUBLISHED)
        context["collection_count"] = viewcols.count()
        return context


class PortalRevisionView(PortalDetailView):
    """Show information about an object revision."""
    def get_context_data(self, **kwargs):
        context = super(PortalRevisionView, self).get_context_data(**kwargs)
        try:
            context["version"] = reversion.get_for_object(self.object).get(
                    id=self.kwargs["revision"])
        except reversion.revisions.Revision.DoesNotExist:
            raise Http404
        messages.add_message(self.request, messages.WARNING, 
                _("You are viewing revision") + " %s" % context["version"].id)
        return context


class PortalRevisionDiffView(PortalDetailView):
    """Show information about an object revision."""
    def get_context_data(self, **kwargs):
        context = super(PortalRevisionDiffView, self).get_context_data(**kwargs)
        try:
            revids = sorted(self.request.GET.getlist("r"))
            context["newversion"] = reversion.get_for_object(self.object).get(
                    id=revids[0])
            context["oldversion"] = reversion.get_for_object(self.object).get(
                    id=revids[1])
        except reversion.revisions.Revision.DoesNotExist, IndexError:
            raise Http404
        messages.add_message(self.request, messages.WARNING, "You are comparing "
            "revisions %s and %s" % (context["newversion"].id, context["oldversion"].id)) 
        return context


class PortalRestoreView(UpdateView):
    """Restore a particular model revision."""
    model = None
    form_class = forms.RestoreRevisionForm
    template_name = "confirm_restore_base.html"

    def get_form(self, *args, **kwargs):
        # NB: Have to override this because otherwise
        # Django tries to instantiate it as it would
        # a modelform (but we don't want a modelform)
        return self.form_class(self.request.POST, self.request.FILES)

    def form_valid(self, form):
        context = self.get_context_data()
        version = context["version"]
        with reversion.create_revision():
            reversion.set_comment("Reverted to '%s'" % version.id)
            version.revert()
            return HttpResponseRedirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PortalRestoreView, self).get_context_data(**kwargs)
        try:
            context["version"] = reversion.get_for_object(self.object).get(
                    id=self.kwargs["revision"])
        except reversion.revisions.Revision.DoesNotExist:
            raise Http404
        return context


    
    
