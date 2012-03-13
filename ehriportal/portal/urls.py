from django.conf.urls.defaults import *

from portal import views, forms

urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchListView.as_view(
        form_class=forms.MapSearchForm,
        template_name="map.html"), name='map_search'),
)
