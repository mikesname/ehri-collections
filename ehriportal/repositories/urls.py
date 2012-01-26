from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from ehriportal.repositories import views

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().facet('country')

urlpatterns = patterns('',
    url(r'^/?$', views.FacetedSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs), name='repos'),
)
