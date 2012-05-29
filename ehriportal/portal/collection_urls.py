
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required, user_passes_test
from haystack.query import SearchQuerySet

from portal import views, utils, forms, models, permissions, nodes
from portal.haystack_util import QueryFacet, FacetClass, QueryFacetClass

FACETS = [
    QueryFacetClass(
        "years",
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
        paramname="langdesc",
        renderfn=utils.language_name_from_code,
    ),
    FacetClass(
        "languages",
        "Language",
        paramname="lang",
        renderfn=utils.language_name_from_code,
    ),
    FacetClass(
        "location_of_materials",
        "Location of Materials",
        paramname="country",
        renderfn=utils.country_name_from_code,
    ),
    FacetClass(
        "tags",
        "Keyword",
        paramname="tag"
    ),
]


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
    url(r'^/?$', views.PortalListView.as_view(
        model=nodes.Collection,
        template_name="collection_list.html",
        ), name='collection_list'),

    # Crud Actions
    url(r'^create/?$', 
            user_passes_test(permissions.is_staff)(
                views.CollectionEditView.as_view(model=nodes.Collection)),
                    name='collection_create'),
    url(r'^edit/(?P<slug>[-\w]+)/?$',
            user_passes_test(permissions.is_staff)(
                views.CollectionEditView.as_view(model=nodes.Collection)), 
                    name='collection_edit'),
    url(r'^delete/(?P<slug>[-\w]+)/?$', 
            user_passes_test(permissions.is_staff)(
                views.CollectionDeleteView.as_view(model=nodes.Collection)), 
                    name='collection_delete'),
    # This URL has to go last because it matches everything...
    url(r'^(?P<slug>[-\w]+)/?$', views.PortalDetailView.as_view(
            model=nodes.Collection,
            template_name="collection_detail.html"
        ), name='collection_detail'),
)

