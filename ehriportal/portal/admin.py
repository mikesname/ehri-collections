"""
Admin config for models.
"""
from django.contrib import admin
from ehriportal.portal.models import Repository, Collection

admin.site.register(Repository)
admin.site.register(Collection)

