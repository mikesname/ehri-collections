from datetime import date
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet, SQ
from haystack.backends import BaseSearchQuery

sqs = SearchQuerySet().models(models.Collection).facet("tags").facet('languages')\
        .facet("location_of_materials")\
        .facet('languages_of_description')

infodict = dict(
        queryset=models.Collection.objects.all()
)


class DatedSearchForm(FacetedSearchForm):
    start_date = date(1933,1,1)
    end_date = date(1946,1,1)

    def search(self):
        sqs = super(DatedSearchForm, self).search()

        sqs = sqs.date_facet("start_date", date(1700,1,1), self.start_date, gap_by="year",
                gap_amount=int(1933-1700))
        for year in range(self.start_date.year, self.end_date.year):
            sqs = sqs.date_facet("date", date(year, 1,1), date(year+1, 1,1), 
                    gap_by="year")
        sqs = sqs.date_facet("end_date", self.end_date, date.today(), gap_by="year",
                gap_amount=int(date.today().year - self.end_date.year))

        return sqs


class CollectionSearchView(FacetedSearchView):
    def extra_context(self, *args, **kwargs):
        extra = super(CollectionSearchView, self).extra_context(*args, **kwargs)

        extra["facet_names"] = dict(
                languages_of_description="Language of Description",
                languages="Language",
                tags="Keyword",
                location_of_materials="Location of Materials"
        )

        #self.searchqueryset = self.searchqueryset\
        #        .date_facet("start_date", date(1700,1,1),
        #            date(1933,1,1), gap_by="year")
        #for i in range(1933, 1946):
        #    self.searchqueryset = self.searchqueryset\
        #            .date_facet("start_date", date(i,1,1),
        #                date(i,1,1), gap_by="year")
        #self.searchqueryset = self.searchqueryset\
        #        .date_facet("start_date", date(1946,1,1),
        #            date.today(), gap_by="year")

        # sort counts, ideally we'd do this in the template
        for facet in extra["facets"]["fields"].keys():
            extra["facets"]["fields"][facet].sort(
                    lambda x, y: cmp(x[0], y[0]))
        print extra["facets"]
        return extra


urlpatterns = patterns('',
    url(r'^/?$', CollectionSearchView(
        form_class=DatedSearchForm, searchqueryset=sqs,
        template="portal/collection_search.html"), name='collection_search'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, infodict, name='collection_detail'),
)

