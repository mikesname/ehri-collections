"""
Portal entities as Bulb Graph nodes.
"""

import os
import sys
import re
import datetime
import json

from django.conf import settings
from django.utils.translation import ugettext as _

from portal import utils, terms

from bulbs import model, property as nodeprop
from bulbs.utils import current_datetime, initialize_element, \
        initialize_elements
from bulbs import neo4jserver

# FIXME: Do away with this global somehow
GRAPH = neo4jserver.Graph() # FIXME: Handle non-default config


class HeldBy(model.Relationship):
    label = "heldBy"
GRAPH.add_proxy(HeldBy.label, HeldBy)


class CreatedBy(model.Relationship):
    label = "createdBy"
GRAPH.add_proxy(CreatedBy.label, CreatedBy)


from django.db.models.query import QuerySet as DjangoQuerySet
from django.db.models.sql import Query as DjangoQuery
from django.db.models.sql.constants import ORDER_PATTERN

class GraphQuery(object):
    def __init__(self, model, where=None):
        self.model = model
        self.low_mark, self.high_mark = 0, None
        self.order_by = []
        self.default_ordering = False
        self.extra_order_by = ()
        self.filters = {}

    def clone(self):
        obj = self.__class__(self.model)
        obj.filters = self.filters.copy()
        obj.low_mark = self.low_mark
        obj.high_mark = self.high_mark
        obj.order_by = self.order_by[:]
        obj.default_ordering = self.default_ordering#
        self.extra_order_by = ()
        return obj

    def combine(self, rhs):
        obj = self.clone()
        obj.filters.update(rhs.filters)
        obj.add_ordering(*rhs.order_by)
        obj.default_ordering = rhs.default_ordering
        return obj

    def add_filter(self, key, value):
        # TODO: No operations supported here except for exact
        # comparison
        obj = self.clone()
        obj.filters[key] = value
        return obj

    def get_count(self, using=None):
        # FIXME: This is all kinds of wrong
        # TODO: Find better way of doing this...
        cmd = "g.V.filter{it.element_type=='%s'}.count()" % self.model.element_type
        number = GRAPH.client.gremlin(cmd).content

        # Apply offset and limit constraints manually, since using LIMIT/OFFSET
        # in SQL (in variants that provide them) doesn't change the COUNT
        # output.
        number = max(0, number - self.low_mark)
        if self.high_mark is not None:
            number = min(number, self.high_mark - self.low_mark)
        return number

    # Methods copied from Django
    # TODO: Inherit these if possible

    def add_ordering(self, *ordering):
        """
        Adds items from the 'ordering' sequence to the query's "order by"
        clause. These items are either field names (not column names) --
        possibly with a direction prefix ('-' or '?') -- or ordinals,
        corresponding to column positions in the 'select' list.

        If 'ordering' is empty, all ordering is cleared from the query.
        """
        errors = []
        for item in ordering:
            if not ORDER_PATTERN.match(item):
                errors.append(item)
        if errors:
            raise FieldError('Invalid order_by arguments: %s' % errors)
        if ordering:
            self.order_by.extend(ordering)
        else:
            self.default_ordering = False

    def clear_ordering(self, force_empty=False):
        """
        Removes any ordering settings. If 'force_empty' is True, there will be
        no ordering in the resulting query (not even the model's default).
        """
        self.order_by = []
        self.extra_order_by = ()
        if force_empty:
            self.default_ordering = False

    def set_limits(self, low=None, high=None):
        """
        Adjusts the limits on the rows retrieved. We use low/high to set these,
        as it makes it more Pythonic to read and write. When the SQL query is
        created, they are converted to the appropriate offset and limit values.

        Any limits passed in here are applied relative to the existing
        constraints. So low is added to the current low value and both will be
        clamped to any existing high value.
        """
        print "Setting limits", low, high
        if high is not None:
            if self.high_mark is not None:
                self.high_mark = min(self.high_mark, self.low_mark + high)
            else:
                self.high_mark = self.low_mark + high
        if low is not None:
            if self.high_mark is not None:
                self.low_mark = min(self.high_mark, self.low_mark + low)
            else:
                self.low_mark = self.low_mark + low

    def clear_limits(self):
        """
        Clears any existing limits.
        """
        self.low_mark, self.high_mark = 0, None

    def can_filter(self):
        """
        Returns True if adding filters to this instance is still possible.

        Typically, this means no limits or offsets have been put on the results.
        """
        return not self.low_mark and self.high_mark is None

    def get_compiler(self, using=None):
        return GremlinCompiler(self)


class GremlinCompiler(object):
    """Class which compiles a GraphQuery into a gremlin query.
    This is a stopgap measure."""
    def __init__(self, query):
        self.query = query

    def get_gremlin_script(self):
        query = self.query
        qstr = "g.V.filter{it.element_type=='%s'}" % query.model.element_type
        for key, value in query.filters.items():
            qstr += ".filter{it.%s==\"%s\"}" % (key, value)
        if query.low_mark != 0 and query.high_mark is None:
            qstr += "._().range(%d, -1)" % query.low_mark
        elif query.low_mark == 0 and query.high_mark is not None:
            qstr += "._().range(0, %d)" % query.high_mark
        elif query.low_mark > 0 and query.high_mark is not None:
            qstr += "._().range(%d, %d)" % (query.low_mark, query.high_mark)

        # TODO: Ordering and stuff
        return qstr

    def results_iter(self):
        script = self.get_gremlin_script()
        for res in initialize_elements(GRAPH.client, GRAPH.client.gremlin(script)):
            yield res


class GraphQuerySet(DjangoQuerySet):
    """Fake QuerySet-like class that mimics (very badly
    at the moment) the Django one."""
    def __init__(self, *args, **kwargs):
        super(GraphQuerySet, self).__init__(*args, **kwargs)
        self.query = kwargs.get("query", GraphQuery(kwargs.get("model")))


    def iterator(self):
        compiler = self.query.get_compiler()
        for res in compiler.results_iter():
            yield res
        
    def filter(self, **kwargs):
        for key, value in kwargs.items():
            self.query = self.query.add_filter(key, value)
        return self.__class__(query=self.query.clone())

    def count(self):
        # TODO: Find better way of doing this...
        cmd = "g.V.filter{it.element_type=='%s'}.count()" % self.model.element_type
        return GRAPH.client.gremlin(cmd).content

    def all(self):
        # TODO: Find a lazy way of doing this
        return 
        

class ResourceType(model.ModelMeta):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, vname, help in attrs.get("translatable_fields", []):
            attrs[fname] = nodeprop.String(name=vname, nullable=True)

        newtype = new(cls, name, bases, attrs)
        # create a proxy in the graph for this type
        if attrs.get("element_type"):
            GRAPH.add_proxy(attrs.get("element_type"), newtype)
        return newtype

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class ResourceBase(model.Node):
    """Mixin for resources holding common properties."""
    __metaclass__ = ResourceType
    __mode__ = model.STRICT
    created_on = nodeprop.DateTime(name=_("Date Created"), nullable=True)
    updated_on = nodeprop.DateTime(name=_("Date Updated"), nullable=True)
    publication_status = nodeprop.Integer(name=_("Publication Status"),
            default=terms.DRAFT, indexed=True, nullable=True)

    def __init__(self, client, **kwargs):
        super(ResourceBase, self).__init__(client)
        self.__dict__.update(**kwargs)

    def _create(self, _data, kwds):
        kwds["created_on"] = kwds.get("created_on", current_datetime())
        return super(ResourceBase, self)._create(_data, kwds)

    def _update(self, _id, _data, kwds):
        kwds["updated_on"] = kwds.get("updated_on", current_datetime())
        return super(ResourceBase, self)._update(_id, _data, kwds)

    def save(self, *args, **kwargs):
        if not self.created_on:
            raise Exception("Unable to save an object created with its own __init__()")
        else:
            self.updated_on = current_datetime()
        return super(ResourceBase, self).save(*args, **kwargs)


class Repository(ResourceBase):
    """Repository."""
    element_type = "repository"
    translatable_fields = (
        ("access_conditions", "Access Conditions", "TODO: Help text"),
        ("buildings", "Buildings", "TODO: Help text"),
        ("collecting_policies", "Collecting Policies", "TODO: Help text"),
        ("dates_of_existence", "Dates of Existence", "TODO: Help text"),
        ("disabled_access", "Disabled Access", "TODO: Help text"),
        ("finding_aids", "Finding Aids", "TODO: Help text"),
        ("functions", "Functions", "TODO: Help text"),
        ("general_context", "General Context", "TODO: Help text"),
        ("geocultural_context", "Geocultural Context", "TODO: Help text"),
        ("history", "History", "TODO: Help text"),
        ("holdings", "Holdings", "TODO: Help text"),
        ("internal_structures", "Internal Structures", "TODO: Help text"),
        ("legal_status", "Legal Status", "TODO: Help text"),
        ("maintenance_notes", "Maintenance Notes", "TODO: Help text"),
        ("mandates", "Mandates", "TODO: Help text"),
        ("opening_times", "Opening Times", "TODO: Help text"),
        ("places", "Places", "TODO: Help text"),
        ("reproduction_services", "Reproduction Services", "TODO: Help text"),
        ("research_services", "Research Services", "TODO: Help text"),
        ("rules", "Rules", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    name = nodeprop.String(name=_("Name"), nullable=False, unique=True)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"))
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    @property
    def collections(self):
        """Get all collections related by the heldBy edge."""
        for edge in self.inE(HeldBy.label):
            yield edge.outV()

    def natural_key(self):
        return (self.name,)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return self.name


class Collection(ResourceBase):
    """Model representing an archival description."""
    element_type = "collection"
    translatable_fields = (
        ("access_conditions", "Access Conditions", "TODO: Help text"),
        ("accruals", "Accruals", "TODO: Help text"),
        ("acquisition", "Immediate source of acquisition or transfer", "TODO: Help text"),
        ("alternate_title", "Alternate Title", "TODO: Help text"),
        ("appraisal", "Appraisal", "TODO: Help text"),
        ("archival_history", "Archival History", "TODO: Help text"),
        ("arrangement", "Arrangement", "TODO: Help text"),
        ("edition", "Edition", "TODO: Help text"),
        ("extent_and_medium", "Extent and Medium", "TODO: Help text"),
        ("finding_aids", "Finding Aids", "TODO: Help text"),
        ("institution_responsible_identifier", "Institution Responsible Identifier", "TODO: Help text"),
        ("location_of_copies", "Location of Copies", "TODO: Help text"),
        ("location_of_originals", "Location of Originals", "TODO: Help text"),
        ("notes", _("Notes"), "TODO: Help text"),
        ("physical_characteristics", "Physical Characteristics", "TODO: Help text"),
        ("related_units_of_description", "Related Units of Description", "TODO: Help text"),
        ("reproduction_conditions", "Reproduction Conditions", "TODO: Help text"),
        ("revision_history", "Revision History", "TODO: Help text"),
        ("rules", "Rules", "TODO: Help text"),
        ("scope_and_content", "Scope and Content", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    name = nodeprop.String(name=_("Title"), nullable=False, unique=True)
    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))
    languages_of_description = nodeprop.List(name=_("Language(s) of Description"))
    scripts_of_description = nodeprop.List(name=_("Script(s) of Description"))

    def get_repository(self):
        try:
            return self.outE(HeldBy.label).next().inV()
        except StopIteration:
            return

    def set_repository(self, repo):
        try:
            rel = self.outE(HeldBy.label).next().eid
            GRAPH.heldBy.delete(rel)
        except StopIteration:
            # this should mean there is no existing repository
            pass
        if repo is not None:
            GRAPH.heldBy.create(self, repo)

    repository = property(get_repository, set_repository)

    def natural_key(self):
        return (self.name,)


class Authority(ResourceBase):
    """Model representing an archival authority."""
    element_type = "authority"
    translatable_fields = (
        ("dates_of_existence", "Dates of Existence", "TODO: Help text"),
        ("functions", "Functions", "TODO: Help text"),
        ("general_context", "General Context", "TODO: Help text"),
        ("history", "History", "TODO: Help text"),
        ("institution_responsible_identifier", "Institution Responsible Identifier", "TODO: Help text"),
        ("internal_structures", "Internal Structures", "TODO: Help text"),
        ("legal_status", "Legal Status", "TODO: Help text"),
        ("mandates", "Mandates", "TODO: Help text"),
        ("places", "Places", "TODO: Help text"),
        ("revision_history", "Revision History", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    name = nodeprop.String(name=_("Authorized Form of Name"), nullable=False)
    level_of_detail = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    def natural_key(self):
        return (self.name,)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return self.name


