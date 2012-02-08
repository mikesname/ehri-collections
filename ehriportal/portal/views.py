# Create your views here.

import re
import datetime
from urllib import quote

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django import forms
from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from portal import models

FACET_SORT_COUNT = 0
FACET_SORT_NAME = 1

INTMATH = re.compile("\[(?:(?P<from>\d{4})|(\*))\sTO\s(?:(?P<to>\d{4})|(\*))\]")

class FacetPoint(object):
    """Class representing a Query Facet point."""
    def __init__(self, point, desc=None):
        self.range = isinstance(point, tuple)
        self.point = point
        self.desc = desc if desc else str(point)

    def __str__(self):
        if self.range:
            return u"[%s TO %s]" % self.point
        return str(self.point)


class DateFacetPoint(object):
    """Specialisation of FacetPoint for dates, where
    each point is either a datetime.datetime object 
    or a string, such as glob ("*")."""
    def _strpoint(self, p):
        if isinstance(p, basestring):
            return p
        return p.isoformat() + "Z"

    def __str__(self):
        if self.range:
            return u"[%s TO %s]" % (self._strpoint(p[0]), self._strpoint(p[1]))
        return str(self.point)
            

class FacetClass(object):
    """Class representing a facet with multiple values
    to filter on. i.e. keywords => [foo, bar ...]"""
    def __init__(self, name, prettyname, sort=FACET_SORT_COUNT):
        self.name = name
        self.prettyname = prettyname
        self.sort = sort
        self.facets = []

    def sorted_facets(self):
        if self.sort == FACET_SORT_COUNT:
            return self.sorted_by_count()
        return self.sorted_by_name()

    def sorted_by_name(self):
        return [f for f in sorted(self.facets, key=lambda k: k.name) \
                if f.count > 0]

    def sorted_by_count(self):
        return [f for f in sorted(self.facets, key=lambda k: -k.count) \
                if f.count > 0]

    def apply(self, queryset):
        """Apply the facet to the search query set."""
        return queryset.facet(self.name)
    
    def parse(self, counts, current):
        """Parse the facet_counts structure returns from
        the Haystack query."""
        self.facets = []
        flist = counts.get("fields", {}).get(self.name)
        for item, count in flist:
            self.facets.append(Facet(self, item, count, current))

    def __repr__(self):
        return u"<%s: %s (%d)" % (
                self.__class__.__name__, self.name, len(self.facets))

    def __unicode__(self):
        return self.prettyname


class QueryFacetClass(FacetClass):
    """Class representing a query facet."""
    def __init__(self, *args, **kwargs):
        self.points = kwargs.pop("points", [])
        super(QueryFacetClass, self).__init__(*args, **kwargs)

    def sorted_by_name(self):
        """Name sort should respect the order in which
        the Query facet points were added in the point spec."""
        return [f for f in self.facets if f.count > 0]

    def parse(self, counts, current):
        self.facets = []
        fqmatch = re.compile("(?P<fname>[^:]+):(?P<query>.+)")
        if not counts.get("queries"):
            return
        for point in self.points:
            count = counts["queries"].get("%s:%s" % (self.name, point))
            self.facets.append(Facet(
                self, str(point), count, current,
                pretty=point.desc, isrange=point.range))

    def apply(self, queryset):
        """Apply the facet to the search query set."""
        for point in self.points:
            queryset = queryset.query_facet(self.name, str(point))
        return queryset


class Facet(object):
    """Class representing an individual facet constraint,
    i.e. 'language:Afrikaans'."""
    def __init__(self, klass, name, count, selected, pretty=None, isrange=False):
        self.name = name
        self.klass = klass
        self.count = count
        self.range = isrange
        self.selected = self.filter_name() in selected
        self.prettyname = pretty if pretty else name

    def filter_name(self):
        if self.range:
            return '%s:%s' % (self.klass.name, self.name)
        # FIXME: Hack for rare facets with '(', ')', etc
        # in the name, need to find a cleaner way of 
        # handling quoting: see 'clean' func in
        # haystack/backends/__init__.py
        def clean(val):
            for char in ['(', ')', '-']:
                val = val.replace(char, '\\%s' % char)
            return val
        return clean('%s:"%s"' % (self.klass.name, self.name))

    def facet_param(self):
        return "sf=%s%%3A%s" % (quote(self.klass.name), quote(self.name))


class SearchForm(forms.Form):
    """Simple search form. Just has a field for the query."""
    q = forms.CharField(required=False, label=_('Search'))

class FacetListSearchForm(SearchForm):
    """Extension of the search form with another field for
    the order in which facets are sorted.  Since we can't do
    this natively with Haystack, we have to hack it ourselves.
    """
    sort = forms.ChoiceField(required=False, 
            choices=(("count",_("Count")), ("name", _("Name"))))


class PortalSearchListView(ListView):
    """A view which performs a search using Haystack and parses
    the facet information into a form that is easily manageable
    for display within the template."""
    model = None
    searchqueryset = None
    paginate_by = 20
    facetclasses = []
    form_class = SearchForm

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
            if self.form.cleaned_data["q"]:
                sqs = sqs.auto_query(self.form.cleaned_data["q"])

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.request.GET.getlist("sf"):
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            # FIXME: everything should be quoted with the
            # exception of MATH ranges ([* TO X]) which 
            # we've constructed ourselves. This is a hacky
            # way of checking for them
            keyval = u'%s:%s' % (field, value)
            if not value.startswith("["):
                keyval = u'%s:"%s"' % (field, sqs.query.clean(value))
            sqs = sqs.narrow(keyval)
        self.searchqueryset = sqs
        return self.searchqueryset

    def get_context_data(self, *args, **kwargs):
        extra = super(PortalSearchListView, self).get_context_data(*args, **kwargs)
        # we need to process out facets in a way that makes it easy to
        # render them without too much horror in the template.
        counts = self.searchqueryset.facet_counts()
        current = self.searchqueryset.query.narrow_queries
        for facetclass in self.facetclasses:
            facetclass.parse(counts, current)
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
    template_name = "portal/facets.html"
    template_name_ajax = "portal/facets_ajax.html"
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

