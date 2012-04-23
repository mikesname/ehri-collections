from django.conf.urls.defaults import *
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required, user_passes_test

from portal import views, forms, models, permissions
from portal.haystack_util import FacetClass

from haystack.query import SearchQuerySet

FACETS = [
    FacetClass(
        "type_of_entity",
        "Authority Type",
    )
]

listinfo = dict(
        queryset=models.Authority.objects.all().order_by("name"),
        paginate_by=20,
        template_name="authority_list.html"
)

class ListCollectionsView(ListView):
    paginate_by = 20
    def get_queryset(self, *args, **kwargs):
        self.authority = get_object_or_404(
                models.Authority, slug=self.kwargs["slug"])
        return models.Collection.objects.filter(creator=self.authority)

    def get_context_data(self, *args, **kwargs):
        extra = super(ListCollectionsView, self).get_context_data(*args, **kwargs)
        extra["authority"] = self.authority
        return extra



urlpatterns = patterns('',
    #url(r'^/?$', object_list, listinfo, name='authority_list'),
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Authority,
        facetclasses=FACETS,
        template_name="authority_search.html"), name='authority_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='authority_search',
        form_class=forms.FacetListSearchForm,
        model=models.Authority,
        facetclasses=FACETS),
            name='authority_facets'),
    url(r'^/?$', object_list, listinfo, name='authority_list'),
    # Crud Actions
    url(r'^create/?$', 
            user_passes_test(permissions.is_staff)(
                views.AuthorityEditView.as_view()), name='authority_create'),
    url(r'^edit/(?P<slug>[-\w]+)/?$',
            user_passes_test(permissions.is_staff)(
                views.AuthorityEditView.as_view()), name='authority_edit'),
    url(r'^delete/(?P<slug>[-\w]+)/?$', 
            user_passes_test(permissions.is_staff)(
                views.AuthorityDeleteView.as_view()), name='authority_delete'),
    url(r'^restore/(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRestoreView.as_view(
            model=models.Authority,
        ), name='authority_restore'),
    url(r'^(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRevisionView.as_view(
            model=models.Authority,
            template_name="authority_revision.html"
        ), name='authority_revision'),
    url(r'^diff/(?P<slug>[-\w]+)/?$', views.PortalRevisionDiffView.as_view(
            model=models.Authority,
            template_name="authority_diff.html",
        ), name='authority_diff'),
    
    # these catch-all item must be at the bottom
    url(r'^(?P<slug>[-\w]+)/?$', views.PortalDetailView.as_view(
            model=models.Authority,
            template_name="authority_detail.html"
        ), name='authority_detail'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            ListCollectionsView.as_view(
                template_name="collection_list.html"    
            ), name='authority_collections'),
)

