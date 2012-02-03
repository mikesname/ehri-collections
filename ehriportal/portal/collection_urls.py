
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, forms, models

from haystack.query import SearchQuerySet

sqs = SearchQuerySet()\
        .models(models.Collection)

FACETS = dict(
    languages_of_description="Language of Description",
    languages="Language",
    tags="Keyword",
    location_of_materials="Location of Materials"
)                                         

DATEPOINTS = [
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

# Facet the SearchQuerySet by our significant dates
# TODO: Fix having to add the 'Z' to the time string
sqs = sqs.query_facet("dates", "[* TO %sZ]" % DATEPOINTS[0].isoformat())
for mark in range(len(DATEPOINTS) - 1):
    sqs = sqs.query_facet("dates", "[%sZ TO %sZ]" % (
        DATEPOINTS[mark].isoformat(), DATEPOINTS[mark+1].isoformat()))
sqs = sqs.query_facet("dates", "[%sZ TO *]" % DATEPOINTS[-1].isoformat())


infolist = dict(
        queryset=models.Collection.objects.all(),
        paginate_by=20
)

viewdict = dict(
        queryset=models.Collection.objects.all()
)


urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchView(
        apply_facets=FACETS, form_class=forms.PortalSearchForm, searchqueryset=sqs,
        template="portal/collection_search.html"), name='collection_search'),
    url(r'^facets/?$', views.PaginatedFacetView(
        apply_facets=FACETS, form_class=forms.PortalSearchForm,
        searchqueryset=sqs),
        name='collection_facets'),
    #url(r'^search/?$', FacetedSearchView(
    #    form_class=FacetedSearchForm, searchqueryset=sqs,
    #    template="portal/collection_search.html"), name='collection_search'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewdict, name='collection_detail'),
)

