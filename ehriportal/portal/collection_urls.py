
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet

from ehriportal.portal import views, forms, models
from ehriportal.portal.views import FacetClass, IntegerFacetClass

FACETS = [
    IntegerFacetClass(
        "years_exact",
        "Date",
        sort=views.FACET_SORT_NAME,
        points=[
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
        form_class=views.FacetListSearchForm,
        model=models.Collection,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewdict, name='collection_detail'),
)

