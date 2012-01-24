from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from ehriportal.repositories import views

urlpatterns = patterns('',
   url(r'^/?$', views.RepoListView.as_view(), name="repos"),
)
