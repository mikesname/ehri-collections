"""
Piston handlers for notable resources.
"""


from piston.handler import BaseHandler
from portal import models


class RepositoryHandler(BaseHandler):
    model = models.Repository


class CollectionHandler(BaseHandler):
    model = models.Collection


class PlaceHandler(BaseHandler):
    model = models.Place


class ContactHandler(BaseHandler):
    model = models.Contact


class AuthorityHandler(BaseHandler):
    model = models.Authority


