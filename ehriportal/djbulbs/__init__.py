"""
Django shim for bulbs stuff.
"""

from bulbs import neo4jserver

# FIXME: Do away with this global somehow
graph = neo4jserver.Graph() # FIXME: Handle non-default config


