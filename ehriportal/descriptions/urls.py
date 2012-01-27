from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from ehriportal.descriptions import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().models(models.Description).facet('languages')\
        .facet('languages_of_description')

urlpatterns = patterns('',
    url(r'^/?$', FacetedSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs,
        template="descriptions/search.html"), name='descriptions'),
)
