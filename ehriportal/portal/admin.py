"""
Admin config for models.
"""
from django.contrib import admin
#from modeltranslation.admin import TranslationAdmin
from portal.models import Repository, Collection, ResourceImage

#class PortalAdmin(TranslationAdmin):
#    """Translatable admin page."""

admin.site.register(Repository)
admin.site.register(Collection)
admin.site.register(ResourceImage)

