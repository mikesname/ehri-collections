"""
Override loaddata so it disconnects Haystack signals before running.
"""
import sys
from django.db.models import signals
from haystack.management.commands.update_index import Command as UpdateIndexCommand, APP, MODEL

from portal import nodes

class Command(UpdateIndexCommand):
    def get_models(self, label):
        from django.db.models import get_app, get_models, get_model
        app_or_model = self.is_app_or_model(label)

        if app_or_model == APP:
            if label == "portal":
                return [nodes.Repository, nodes.Authority, nodes.Collection]
            app_mod = get_app(label)
            return get_models(app_mod)
        else:
            app_label, model_name = label.split('.')
            if app_label == "portal":
                return [getattr(nodes, model_name)]
            return [get_model(app_label, model_name)]


