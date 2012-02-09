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
    def get_form_kwargs(self):
        kwargs = super(CreateSuggestionView, self).get_form_kwargs()
        if self.request.is_ajax():
            kwargs.update({'prefix': "suggestion"})
        return kwargs

    def form_valid(self, form):
        """Extract the instance from the form and insert
        request metadata."""
        object = form.instance
        object.meta = models.get_suggestion_meta(self.request)
        return super(CreateSuggestionView, self).form_valid(form)

    def get_template_names(self):
        if self.request.is_ajax():
            return ["suggestions/suggestion_form_ajax.html"]
        return ["suggestions/suggestion_form.html"]

urlpatterns = patterns('',
    url(r'^create/?$', CreateSuggestionView.as_view(
            form_class=forms.SuggestionForm),
                name='suggestion_create'),
    url(r'^detail/(?P<object_id>\d+)/?$', object_detail, listdict,
            name="suggestion_detail"),
    url(r'^list/?$', object_list, listdict,
            name="suggestion_list"),
)

