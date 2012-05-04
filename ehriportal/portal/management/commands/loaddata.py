"""
Override loaddata so it disconnects Haystack signals before running.
"""
import sys
from django.db.models import signals
from django.core.management.commands.loaddata import Command as LoadDataCommand

class Command(LoadDataCommand):
    def handle(self, *args, **kwargs):
        # disconnect Haystack realtime signals
        signals.pre_save.disconnect(dispatch_uid="setup_index_signals")
        signals.pre_delete.disconnect(dispatch_uid="setup_index_signals")
        return super(Command, self).handle(*args, **kwargs)

