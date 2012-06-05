"""
Override loaddata so it disconnects Haystack signals before running.
"""
import sys
from django.db.models import signals
from haystack.management.commands.update_index import Command as UpdateIndexCommand

from portal import nodes

class Command(UpdateIndexCommand):
    def get_models(self, *args, **kwargs):
        models = super(Command, self).get_models(*args, **kwargs)
        if not models:
            models = [nodes.Repository, nodes.Collection, nodes.Authority]
        return models


