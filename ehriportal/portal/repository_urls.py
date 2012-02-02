from django.conf.urls.defaults import *
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().models(models.Repository).facet('country')

listinfo = dict(
        queryset=models.Repository.objects.all().order_by("name"),
        paginate_by=20
)

viewinfo = dict(
        queryset=models.Repository.objects.all(),
)

class RepoEditForm(ModelForm):
    class Meta:
        model = models.Repository


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

class RepoSearchForm(FacetedSearchForm):
    def no_query_found(self):
        print "No query found!"
        """Show all results when not given a query."""
        sqs = self.searchqueryset.all()
        print sqs
        if self.load_all:
            print "Loading all"
            sqs = sqs.load_all()
        return sqs



class RepoSearchView(FacetedSearchView):
    def extra_context(self, *args, **kwargs):
        extra = super(RepoSearchView, self).extra_context(*args, **kwargs)
        extra["query"] = self.query
        extra["facet_names"] = dict(
                country="Country"
        )

        # sort counts, ideally we'd do this in the template
        if extra.get("facets") and extra.get("facets").get("fields"):
            for facet in extra["facets"]["fields"].keys():
                extra["facets"]["fields"][facet].sort(
                        lambda x, y: cmp(x[0], y[0]))
        return extra

    def build_page(self, *args, **kwargs):
        res = super(RepoSearchView, self).build_page(*args, **kwargs)
        print "RESULTS %s" % self.results
        print "BUILT PAGE: %s %s" % res
        print "COUNT: %s" % res[0].count
        return res


urlpatterns = patterns('',
    #url(r'^/?$', object_list, listinfo, name='repo_list'),
    url(r'^search/?$', RepoSearchView(
        form_class=RepoSearchForm, searchqueryset=sqs,
        template="portal/repository_search.html"), name='repo_search'),
    url(r'^/?$', object_list, listinfo, name='repo_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewinfo, name='repo_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/?$', update_object, dict(
            form_class=RepoEditForm
        ), name='repo_edit'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            ListCollectionsView.as_view(), name='repo_collections'),
)

