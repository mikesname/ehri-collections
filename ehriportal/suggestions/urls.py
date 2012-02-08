"""Suggestion URLs."""

from os import path
from django.conf.urls.defaults import *
from django.views.generic import CreateView
from django.views.generic.list_detail import object_detail, object_list

from suggestions import forms, models

infodict = dict(
        model=models.Suggestion
)

listdict = dict(
        queryset=models.Suggestion.objects.all()
)

class CreateSuggestionView(CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["suggestions/suggestion_form_ajax.html"]
        return ["suggestions/suggestion_form.html"]

urlpatterns = patterns('',
    url(r'^create/?$', CreateSuggestionView.as_view(
            form_class=forms.SuggestionForm), name='suggestion_create'),
    url(r'^detail/(?P<object_id>\d+)/?$', object_detail, listdict,
            name="suggestion_detail"),
    url(r'^list/?$', object_list, listdict,
            name="suggestion_list"),
)

