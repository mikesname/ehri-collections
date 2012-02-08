
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet

from portal import views, forms, models
from portal.views import FacetPoint, FacetClass, QueryFacetClass

FACETS = [
    QueryFacetClass(
        "years_exact",
        "Date",
        sort=views.FACET_SORT_NAME,
        points=[
            FacetPoint(("*", 1933), "Before 1933"),
            FacetPoint((1933, 1939), "1933-1939"),
            FacetPoint(1940),
            FacetPoint(1941),
            FacetPoint(1942),
            FacetPoint(1943),
            FacetPoint(1944),
            FacetPoint(1945),
            FacetPoint((1946, "*"), "After 1945"),
        ]
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

infolist = dict(
        queryset=models.Collection.objects.all(),
        paginate_by=20
)

viewdict = dict(
        queryset=models.Collection.objects.all()
)

urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Collection,
        template_name="portal/collection_search.html",
        facetclasses = FACETS),
            name='collection_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='collection_search',
        form_class=views.FacetListSearchForm,
        model=models.Collection,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewdict, name='collection_detail'),
)

