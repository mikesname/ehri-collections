
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet, SQ
from haystack.backends import BaseSearchQuery

sqs = SearchQuerySet()\
        .models(models.Collection)\
        .facet("tags").facet('languages')\
        .facet("location_of_materials")\
        .facet('languages_of_description')

infolist = dict(
        queryset=models.Collection.objects.all(),
        paginate_by=20
)

viewdict = dict(
        queryset=models.Collection.objects.all()
)


# Crime against programming
DATEMATH = re.compile("\[(?:(?P<from>\d{4})|(\*))[\s-].*?TO (?:(?P<to>\d{4})|(\*)).*?\]")


class DatedSearchForm(FacetedSearchForm):
    def search(self):
        """Override FacetedSearchForm to not quote ranged facets."""

    def search(self):        
        datemarks = [
                datetime(1933,1,1),
                datetime(1939,1,1),
                datetime(1940,1,1),
                datetime(1941,1,1),
                datetime(1942,1,1),
                datetime(1943,1,1),
                datetime(1944,1,1),
                datetime(1945,1,1),
                datetime(1946,1,1),
        ]

        sqs = super(FacetedSearchForm, self).search()
        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            # FIXME: This part overrides the base class so that
            # facet values that match a date math string are NOT
            # quoted, which screws them up.  This is unfortunate 
            # and a better way needs to be found
            if value:
                keyval = u'%s:"%s"' % (field, sqs.query.clean(value))
                if DATEMATH.match(value):
                    keyval = u'%s:%s' % (field, value)
                sqs = sqs.narrow(keyval)
        
        # TODO: Fix having to add the 'Z' to the time string
        sqs = sqs.query_facet("dates", "[* TO %sZ]" % datemarks[0].isoformat())
        for mark in range(len(datemarks) - 1):
            sqs = sqs.query_facet("dates", "[%sZ TO %sZ]" % (
                datemarks[mark].isoformat(), datemarks[mark+1].isoformat()))
        sqs = sqs.query_facet("dates", "[%sZ TO *]" % datemarks[-1].isoformat())        

        return sqs

    def no_query_found(self):
        """Show all results when not given a query."""
        sqs = self.searchqueryset.all()
        if self.load_all:
            sqs = sqs.load_all()
        return sqs


class CollectionSearchView(FacetedSearchView):
    def extra_context(self, *args, **kwargs):
        extra = super(CollectionSearchView, self).extra_context(*args, **kwargs)
        extra["query"] = self.query
        extra["facet_names"] = dict(
                languages_of_description="Language of Description",
                languages="Language",
                tags="Keyword",
                location_of_materials="Location of Materials"
        )

        # sort counts, ideally we'd do this in the template
        if extra.get("facets") and extra.get("facets").get("fields"):
            for facet in extra["facets"]["fields"].keys():
                extra["facets"]["fields"][facet].sort(
                        lambda x, y: cmp(x[0], y[0]))

        # this is oh so gross at the moment. Now I have two problems...
        dmatch = re.compile("dates:(?P<facet>" + DATEMATH.pattern + ")")
        if extra.get("facets") and extra.get("facets").get("queries"):
            query_facets = []
            for facet, num in extra["facets"]["queries"].iteritems():
                mf = dmatch.match(facet)
                if mf:
                    query_facets.append({
                        "facet": mf.group("facet"),
                        "count": int(num),
                        "from":  mf.group("from"),
                        "to"  :  mf.group("to")
                    })
            extra["query_facets"] = sorted(query_facets, key=lambda k: k["from"])
            # make pretty strings for display of glob facets
            for i in range(len(extra["query_facets"])):
                f = extra["query_facets"][i]
                s = "%s-%s" % (f["from"], f["to"])
                if f["from"] is None:
                    s = "Before %s" % f["to"]
                elif f["to"] is None:
                    s = "Since %s" % f["from"]
                extra["query_facets"][i]["str"] = s
        return extra



urlpatterns = patterns('',
    url(r'^search/?$', CollectionSearchView(
        form_class=DatedSearchForm, searchqueryset=sqs,
        template="portal/collection_search.html"), name='collection_search'),
    #url(r'^search/?$', FacetedSearchView(
    #    form_class=FacetedSearchForm, searchqueryset=sqs,
    #    template="portal/collection_search.html"), name='collection_search'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewdict, name='collection_detail'),
)

