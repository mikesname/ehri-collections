from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    # this bare URL crops up mysteriously in production... 
    # redirect it to the account login page.
    url(r"^openid/?$", redirect_to, {"url": reverse_lazy("acct_login"), "permanent": True}),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    #url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^repositories/", include("portal.repository_urls")),
    url(r"^collections/", include("portal.collection_urls")),
    url(r"^authorities/", include("portal.authority_urls")),
    url(r"^suggestions/", include("suggestions.urls")),
    url(r"^search/", include("portal.urls")),
    url(r"^api/", include("portal.api.urls")),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls"), {
            'document_root': settings.MEDIA_ROOT,    
        }),
        url("^site_media/media(?P<path>.*)$", 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
