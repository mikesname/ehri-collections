"""
Admin config for models.
"""
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from ehriportal.portal.models import Repository, Collection

class PortalAdmin(TranslationAdmin):
    """Translatable admin page."""

admin.site.register(Repository, PortalAdmin)
admin.site.register(Collection)

