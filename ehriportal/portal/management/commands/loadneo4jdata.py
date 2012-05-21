"""
Override loaddata so it disconnects Haystack signals before running.
"""
import os
import sys
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.commands.loaddata import Command as LoadDataCommand

from bulbs import neo4jserver
from bulbs.config import DEBUG

# FIXME: Do away with this global somehow
GRAPH = neo4jserver.Graph() # FIXME: Handle non-default config

class Command(BaseCommand):

    args = "fixture [fixture ...]"
    option_list = BaseCommand.option_list + ()

    def handle(self, *fixture_labels, **options):
        verbosity = int(options.get('verbosity'))
        show_traceback = options.get('traceback')        
        if not len(fixture_labels):
            self.stderr.write(
                self.style.ERROR("No database fixture specified. Please provide "
                    "the path of at least one fixture in the command line.\n")
            )
            return

        fixture_count = 0
        loaded_object_count = 0
        fixture_object_count = 0
        models = set()

        scripts_file = os.path.join(settings.PROJECT_ROOT, "portal", "gremlin.groovy")
        GRAPH.client.scripts.update(scripts_file)

        for fixture in fixture_labels:
            sys.stderr.write("Loading fixture: %s\n" % fixture)
            with open(fixture, "r") as fh:
                objects = json.load(fh, encoding="utf8")
                for i in range(len(objects)):
                    object = objects[i]
                    data = object["fields"]
                    if verbosity > 2:
                        sys.stderr.write("Loading %04d %s\n" % (i, data.get("name")))
                    # temp hacks
                    data["element_type"] = object["model"].split(".")[1]
                    data["lod"] = None
                    data["type_of_entity"] = None
                    data.pop("languages_of_description", None)
                    data.pop("languages", None)
                    data.pop("scripts_of_description", None)
                    data.pop("scripts", None)
            script = GRAPH.client.scripts.get("ingest_portal_data")
            res = GRAPH.client.gremlin(script, params=dict(data=objects))
            print res.content
