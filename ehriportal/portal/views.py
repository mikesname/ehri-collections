# Create your views here.

import re
from urllib import quote

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django import forms
from django.conf import settings

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from ehriportal.portal import models

# Crime against programming - regexes to match
# '[* TO 1928-01-01T00:00:00Z]' and [* TO 1939]
DATEMATH = re.compile("\[(?:(?P<from>\d{4})|(\*))[\s-].*?TO (?:(?P<to>\d{4})|(\*)).*?\]")
INTMATH = re.compile("\[(?:(?P<from>\d{4})|(\*))\sTO\s(?:(?P<to>\d{4})|(\*))\]")

FACET_SORT_COUNT = 0
FACET_SORT_NAME = 1

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
    querymatch = re.compile("DUMMY")
    """Abstract class representing a query facet.  Derived classes
    must supply a querymatch that matches the type of ranges being
    operated on, i.e. dates or integers."""
    def parse(self, counts, current):
        self.facets = []
        fqmatch = re.compile("(?P<fname>[^:]+):(?P<facet>" + self.querymatch + ")")
        if not counts.get("queries"):
            return
        for facet, count in counts["queries"].iteritems():
            mf = fqmatch.match(facet)
            if not mf or not mf.group("fname") == self.name:
                continue
            name = mf.group("facet")
            facet = Facet(self, mf.group("facet"), count, current, query=True)
            if mf.group("from") is None:
                facet.prettyname = "Before %s" % mf.group("to")
            elif mf.group("to") is None:
                facet.prettyname = "From %s" % mf.group("from")
            else:
                facet.prettyname = "%s-%s" % (mf.group("from"), mf.group("to"))
            self.facets.append(facet)


class IntegerFacetClass(QueryFacetClass):
    querymatch = INTMATH.pattern


class DateFacetClass(QueryFacetClass):
    querymatch = DATEMATH.pattern


class Facet(object):
    def __init__(self, klass, name, count, selected, pretty=None, query=False):
        self.name = name
        self.klass = klass
        self.count = count
        self.query = query
        self.selected = self.filter_name() in selected
        self.prettyname = pretty if pretty else name

    def filter_name(self):
        if self.query:
            return '%s:%s' % (self.klass.name, self.name)
        return '%s:"%s"' % (self.klass.name, self.name)

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
        sqs = self.searchqueryset.models(self.model)
        for facet in self.facetclasses:
            sqs = sqs.facet(facet.name)

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
            # FIXME: This part overrides the base class so that
            # facet values that match a date math string are NOT
            # quoted, which screws them up.  This is unfortunate 
            # and a better way needs to be found
            if value:
                keyval = u'%s:"%s"' % (field, sqs.query.clean(value))
                if INTMATH.match(value):
                    keyval = u'%s:%s' % (field, value)
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
    
    def __init__(self, *args, **kwargs):
        super(PaginatedFacetView, self).__init__(*args, **kwargs)
        self.fclass = None

    def get_queryset(self):
        sqs = super(PaginatedFacetView, self).get_queryset()
        # look for the active facet
        counts = self.searchqueryset.facet_counts()
        current = self.searchqueryset.query.narrow_queries
        self.fclass = [fc for fc in self.facetclasses \
                if fc.name == self.kwargs["facet"]][0]
        self.fclass.parse(counts, current)
        if self.form.cleaned_data["sort"] == "count":
            return [f for f in self.fclass.sorted_by_count() if f.count]
        return [f for f in self.fclass.sorted_by_name() if f.count]

    def get_template_names(self, **kwargs):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        extra = super(PaginatedFacetView, self).get_context_data(**kwargs)
        extra["facetclass"] = self.fclass
        # hack! which tells us where to redirect to again
        extra["redirect"] = re.sub("/" + self.kwargs["facet"] + "/?",
                "", self.request.get_full_path())
        return extra

