"""
Admin config for suggestions.
"""
from django.contrib import admin
from suggestions.models import Suggestion

admin.site.register(Suggestion)


