
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet

from portal import views, forms, models
from portal.haystack_util import QueryFacet, FacetClass, QueryFacetClass

FACETS = [
    QueryFacetClass(
        "years_exact",
        "Date",
        paramname="date",
        sort=FacetClass.FACET_SORT_NAME,
        queries=[
            QueryFacet(query=("*", 1933), desc="Before 1933"),
            QueryFacet(query=(1933, 1939), desc="1933-1939"),
            QueryFacet(query=1940),
            QueryFacet(query=1941),
            QueryFacet(query=1942),
            QueryFacet(query=1943),
            QueryFacet(query=1944),
            QueryFacet(query=1945),
            QueryFacet(query=(1946, "*"), desc="After 1945"),
        ]
    ),
    FacetClass(
        "languages_of_description",
        "Language of Description",
        paramname="langdesc"
    ),
    FacetClass(
        "languages",
        "Language",
        paramname="lang"
    ),
    FacetClass(
        "location_of_materials",
        "Location of Materials",
        paramname="country",
    ),
    FacetClass(
        "tags",
        "Keyword",
        paramname="tag"
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
        template_name="collection_search.html",
        facetclasses = FACETS),
            name='collection_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='collection_search',
        form_class=forms.FacetListSearchForm,
        model=models.Collection,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, infolist, name='collection_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, dict(
            queryset=models.Collection.objects.all(),
            template_name="collection_detail.html"
        ), name='collection_detail'),
)

