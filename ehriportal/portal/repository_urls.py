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
        "country",
        "Country",
    )
]

listinfo = dict(
        queryset=models.Repository.objects.all().order_by("name"),
        paginate_by=20,
        template_name="repository_list.html"
)

viewinfo = dict(
        queryset=models.Repository.objects.all(),
)

class ListCollectionsView(ListView):
    paginate_by = 20
    def get_queryset(self, *args, **kwargs):
        self.repository = get_object_or_404(
                models.Repository, slug=self.kwargs["slug"])
        return models.Collection.objects.filter(repository=self.repository)

    def get_context_data(self, *args, **kwargs):
        extra = super(ListCollectionsView, self).get_context_data(*args, **kwargs)
        extra["repository"] = self.repository
        return extra



urlpatterns = patterns('',
    #url(r'^/?$', object_list, listinfo, name='repository_list'),
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Repository,
        facetclasses=FACETS,
        template_name="repository_search.html"), name='repository_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='repository_search',
        form_class=forms.FacetListSearchForm,
        model=models.Repository,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, listinfo, name='repository_list'),
    # Crud Actions
    url(r'^create/?$', 
            user_passes_test(permissions.is_staff)(
                views.RepositoryEditView.as_view()), name='repository_create'),
    url(r'^edit/(?P<slug>[-\w]+)/?$',
            user_passes_test(permissions.is_staff)(
                views.RepositoryEditView.as_view()), name='repository_edit'),
    url(r'^delete/(?P<slug>[-\w]+)/?$', 
            user_passes_test(permissions.is_staff)(
                views.RepositoryDeleteView.as_view()), name='repository_delete'),
    url(r'^history/(?P<slug>[-\w]+)/?$', views.PortalHistoryView.as_view(
            model=models.Repository,
        ), name='repository_history'),
    url(r'^restore/(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRestoreView.as_view(
            model=models.Repository,
        ), name='repository_restore'),
    url(r'^diff/(?P<slug>[-\w]+)/?$', views.PortalRevisionDiffView.as_view(
            model=models.Repository,
            template_name="repository_diff.html",
        ), name='repository_diff'),
    
    # these catch-all item must be at the bottom
    url(r'^(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRevisionView.as_view(
            model=models.Repository,
            template_name="repository_revision.html"
        ), name='repository_revision'),
    url(r'^(?P<slug>[-\w]+)/?$', views.PortalDetailView.as_view(
            model=models.Repository,
            template_name="repository_detail.html"
        ), name='repository_detail'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            ListCollectionsView.as_view(
                template_name="collection_list.html"    
            ), name='repository_collections'),
)

