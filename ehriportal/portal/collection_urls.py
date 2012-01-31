from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().models(models.Collection).facet("tags").facet('languages')\
        .facet("location_of_materials")\
        .facet("start_date")\
        .facet('languages_of_description')

infodict = dict(
        queryset=models.Collection.objects.all()
)

class CollectionSearchView(FacetedSearchView):
    def extra_context(self, *args, **kwargs):
        extra = super(CollectionSearchView, self).extra_context(*args, **kwargs)
        extra["facet_names"] = dict(
                languages_of_description="Language of Description",
                languages="Language",
                tags="Keyword",
                start_date="Start Date",
                location_of_materials="Location of Materials"
        )
        # sort counts, ideally we'd do this in the template
        for facet in extra["facets"]["fields"].keys():
            extra["facets"]["fields"][facet].sort(
                    lambda x, y: cmp(x[0], y[0]))
        print extra["facets"]["fields"]
        return extra


urlpatterns = patterns('',
    url(r'^/?$', CollectionSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs,
        template="portal/collection_search.html"), name='collection_search'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, infodict, name='collection_detail'),
)

