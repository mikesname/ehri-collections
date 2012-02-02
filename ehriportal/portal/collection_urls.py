
import re
from datetime import date
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet, SQ
from haystack.backends import BaseSearchQuery

sqs = SearchQuerySet().models(models.Collection).facet("tags").facet('languages')\
        .facet("location_of_materials")\
        .facet('languages_of_description')

infolist = dict(
        queryset=models.Collection.objects.all(),
        paginate_by=20
)

viewdict = dict(
        queryset=models.Collection.objects.all()
)


class DatedSearchForm(FacetedSearchForm):
    start_date = date(1933,1,1)
    end_date = date(1946,1,1)

    def search(self):
        sqs = super(DatedSearchForm, self).search()

        sqs = sqs.date_facet("dates", self.start_date, self.end_date, 
                    gap_by="year")

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

        # extract the actual date facets for easy listing
        if extra.get("facets") and extra.get("facets").get("dates"):
            date_facets = []
            for facet, num in extra["facets"]["dates"]["dates"].iteritems():
                mf = re.match("^(?P<year>\d{4})-\d{2}-\d{2}.*", facet)
                if mf:
                    date_facets.append((facet, int(num)))
            date_facets.sort(lambda x, y: cmp(x[0], y[0]))
            extra["date_facets"] = date_facets
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

