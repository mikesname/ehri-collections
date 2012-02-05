
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, forms, models

from haystack.query import SearchQuerySet

sqs = SearchQuerySet()\
        .models(models.Collection)

from ehriportal.portal.views import FacetClass, IntegerFacetClass

FACETS = [
    IntegerFacetClass(
        "years_exact",
        "Date",
        sort=views.FACET_SORT_NAME
    ),
    FacetClass(
        "languages_of_description",
        "Language of Description"
    ),
    FacetClass(
        "languages",
        "Language"
    ),
    FacetClass(
        "location_of_materials",
        "Location of Materials"
    ),
    FacetClass(
        "tags",
        "Keyword"
    ),
]

DATEPOINTS = [
        1933,
        1939,
        1940,
        1941,
        1942,
        1943,
        1944,
        1945,
        1946,
]

# Facet the SearchQuerySet by our significant dates
# TODO: Fix having to add the 'Z' to the time string
sqs = sqs.query_facet("years", "[* TO %d]" % DATEPOINTS[0])
for mark in range(len(DATEPOINTS) - 1):
    sqs = sqs.query_facet("years", "[%d TO %d]" % (
        DATEPOINTS[mark], DATEPOINTS[mark+1]))
sqs = sqs.query_facet("years", "[%s TO *]" % DATEPOINTS[-1])


infolist = dict(
        queryset=models.Collection.objects.all(),
        paginate_by=20
)

viewdict = dict(
        queryset=models.Collection.objects.all()
)


urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchListView.as_view(
        searchqueryset=sqs,
        model=models.Collection,
        template_name="portal/collection_search.html",
        facetclasses = FACETS), name='collection_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        form_class=views.FacetListSearchForm,
        searchqueryset=sqs,
        model=models.Collection,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewdict, name='collection_detail'),
)

