"""
Portal entities as Bulb Graph nodes.
"""

import os
import sys
import re
import datetime
import json

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str, force_unicode

from portal import utils, terms, models

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


class MentionedIn(model.Relationship):
    label - "mentionedIn"
GRAPH.add_proxy(MentionedIn.label, MentionedIn)




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
        self.start = "g.V"

    def clone(self):
        obj = self.__class__(self.model)
        obj.filters = self.filters.copy()
        obj.low_mark = self.low_mark
        obj.high_mark = self.high_mark
        obj.order_by = self.order_by[:]
        obj.default_ordering = self.default_ordering#
        obj.start = self.start
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

    def set_start(self, str):
        obj = self.clone()
        obj.start = str
        return obj

    def get_count(self, using=None):
        # FIXME: This is all kinds of wrong
        # TODO: Find better way of doing this...
        script = self.get_compiler().get_gremlin_script()
        number = GRAPH.client.gremlin("%s.count()" % script).content

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

    def __iter__(self):
        compiler = self.get_compiler()
        for iter in compiler.results_iter():
            yield iter


class GremlinCompiler(object):
    """Class which compiles a GraphQuery into a gremlin query.
    This is a stopgap measure."""
    def __init__(self, query):
        self.query = query

    def get_gremlin_script(self):
        query = self.query
        # short cut for starting traversal from a particular
        # point. Defaults to g.V (all verts)
        start = self.query.start
        qstr = "%s.filter{it.element_type=='%s'}" % (start, query.model.element_type)
        for key, value in query.filters.items():
            qstr += ".filter{it.%s==\"%s\"}" % (key, value)
        
        # TODO: Desc/Asc ordering
        if self.query.order_by:
            for item in self.query.order_by:
                qstr += ".sort{it.%s}" % item
        # TODO: Default ordering
        
        if query.low_mark != 0 and query.high_mark is None:
            qstr += "._().range(%d, -1)" % query.low_mark
        elif query.low_mark == 0 and query.high_mark is not None:
            qstr += "._().range(0, %d)" % query.high_mark
        elif query.low_mark > 0 and query.high_mark is not None:
            qstr += "._().range(%d, %d)" % (query.low_mark, query.high_mark)

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
        self.query = kwargs.get("query", GraphQuery(self.model))

    def start_from(self, gremlinstr):
        """Hacky method to change the starting point of
        a graph traversal queryset. By default it's
        g.V (all vertices)."""
        clone = self._clone()
        clone.query = clone.query.set_start(gremlinstr)
        return clone

    def iterator(self):
        compiler = self.query.get_compiler()
        for res in compiler.results_iter():
            yield res
        
    def filter(self, **kwargs):
        clone = self._clone()
        for key, value in kwargs.items():
            clone.query = clone.query.add_filter(key, value)
        return clone

    def count(self):
        return self.query.get_count()

    def all(self):
        # TODO: Find a lazy way of doing this
        return self._clone()

    def create(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        self._for_write = True
        proxy = getattr(GRAPH, self.model.element_type)
        return proxy.create(**kwargs)

    def get(self, **kwargs):
        clone = self.filter(**kwargs)
        if self.query.can_filter():
            clone = clone.order_by()
        num = len(clone)
        if num == 1:
            return clone._result_cache[0]
        if not num:
            raise self.model.DoesNotExist(
                "%s matching query does not exist. "
                "Lookup parameters were %s" %
                (self.model.__class__.__name__, kwargs))
        raise self.model.MultipleObjectsReturned(
            "get() returned more than one %s -- it returned %s! "
            "Lookup parameters were %s" %
            (self.model.__class__.__name__, num, kwargs))

    def get_or_create(self, **kwargs):
        assert kwargs, \
                'get_or_create() must be passed at least one keyword argument'
        defaults = kwargs.pop("defaults",{})
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            pass
        data = defaults.copy()
        data.update(**kwargs)
        return self.create(**data), True



from django.db.models.manager import Manager, ManagerDescriptor

class GraphManager(Manager):
    """Mock manager for graph models."""
    def get_query_set(self):
        return GraphQuerySet(self.model)

    def contribute_to_class(self, model, name):
        self.model = model
        mandesc = ManagerDescriptor(self)
        setattr(model, name, mandesc)
        setattr(model, "_default_manager", mandesc)

    def create(self, **kwargs):
        qs = self.get_query_set()
        return super(GraphManager, self).create(**kwargs)


from django.db.models.options import Options


class ResourceType(model.ModelMeta):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):

        super_new = super(ResourceType, cls).__new__
        parents = [b for b in bases if isinstance(b, ResourceType)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, '_meta', None)

        if getattr(meta, 'app_label', None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            model_module = sys.modules[new_class.__module__]
            kwargs = {"app_label": model_module.__name__.split('.')[-2]}
        else:
            kwargs = {}

        new_class.add_to_class('_meta', Options(meta, **kwargs))


         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return super_new(cls, name, bases, attrs)
        
        # Add translatable fields
        for fname, vname, help in attrs.get("translatable_fields", []):
            new_class.add_to_class(fname, nodeprop.String(name=vname, nullable=True))

        # Add other attributes
        for name, obj in attrs.items():
            new_class.add_to_class(name, obj)

        return new_class

    # Try and make some Django magic happy
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


from django.core.exceptions import (ObjectDoesNotExist, 
            MultipleObjectsReturned)

class ResourceBase(model.Node, models.EntityUrlMixin):
    """Mixin for resources holding common properties."""
    # Publication status enum
    DRAFT, PUBLISHED = range(2)
    PUB_STATUS = (
            (DRAFT, _("Draft")),
            (PUBLISHED, _("Published")),
    )

    __metaclass__ = ResourceType
    __mode__ = model.STRICT
    name = nodeprop.String(name=_("Name"), unique=True, indexed=True, nullable=False)
    slug = nodeprop.String(name=_("Slug"), unique=True, indexed=True, nullable=False)
    created_on = nodeprop.DateTime(name=_("Date Created"), nullable=False)
    updated_on = nodeprop.DateTime(name=_("Date Updated"), nullable=True)
    publication_status = nodeprop.Integer(name=_("Publication Status"),
            default=DRAFT, indexed=True, nullable=True)

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    def __init__(self, client, **kwargs):
        super(ResourceBase, self).__init__(client)
        self.__dict__.update(**kwargs)

    def _get_slug(self, name):
        proxy = getattr(GRAPH, self.element_type)
        initial = 2
        base = slugify(name)
        potential = base
        while True:
            ires = proxy.index.lookup(slug=potential)
            if len(list(ires)) == 0:
                break
            potential = u"%s-%d" % (base, initial)
            initial += 1
        return potential

    def __unicode__(self):                                                 

        return self.name

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        return '%s object' % self.__class__.__name__

    def __repr__(self):
        return u"<%s: %s>" % (self.__class__.__name__, self.slug)

    @property
    def resource_type(self):
        return self._meta.verbose_name

    @property
    def published(self):
        return self.publication_status == self.PUBLISHED

    def _create(self, _data, kwds):
        kwds["created_on"] = kwds.get("created_on", current_datetime())
        # get the slug from the name
        kwds["slug"] = self._get_slug(kwds["name"])
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

    lod = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"))
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    @property
    def collection_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('heldBy').outV" % self.eid)

    @property
    def collections(self):
        """Get all collections related by the heldBy edge."""
        for edge in self.inE(HeldBy.label):
            yield edge.outV()

    def natural_key(self):
        return (self.name,)
GRAPH.add_proxy(Repository.element_type, Repository)


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

    objects = GraphManager()

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    lod = nodeprop.Integer(name=_("Level of Description"))
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
GRAPH.add_proxy(Collection.element_type, Collection)


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

    @property
    def collection_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('createdBy').outV" % self.eid)

    @property
    def mentioned_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('mentionedIn').outV" % self.eid)

    lod = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    def natural_key(self):
        return (self.name,)
GRAPH.add_proxy(Authority.element_type, Authority)

