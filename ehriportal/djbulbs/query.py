"""
Django Shims for Bulbs models.
"""

import os
import copy
import datetime

from django.db.models.query import QuerySet, ValuesQuerySet, ValuesListQuerySet
from django.db.models.sql import Query as DjangoQuery
from django.db.models.sql.constants import ORDER_PATTERN, LOOKUP_SEP

from bulbs.utils import initialize_elements, to_timestamp

from . import graph as GRAPH


scripts_file = os.path.join(os.path.dirname(__file__), "gremlin.groovy")
GRAPH.client.scripts.update(scripts_file)

OPS = (
    "exact",
    "iexact",
    "startswith",
    "endswith",
    "contains",
    "gt",
    "lt",
    "gte",
    "lte",
)


class GraphCompiler(object):
    def __init__(self, query, db):
        self.query = query
        self.db = db

    def results_iter(self):
        params = self.query.get_query_params()
        script = GRAPH.client.scripts.get("query")
        results = GRAPH.client.gremlin(script, params=params)
        for res in initialize_elements(GRAPH.client, results):
            yield res


class GraphQuery(object):
    def __init__(self, model, where=None):
        self.model = model
        self.db = GRAPH
        self.low_mark, self.high_mark = 0, None
        self.order_by = []
        self.default_ordering = False
        self.extra_order_by = ()
        self.filters = {}
        self.relations = []

    def clear_deferred_loading(self):
        pass

    def clear_select_fields(self):
        pass

    def add_fields(self, *args, **kwargs):
        pass

    def get_compiler(self, db=None):
        return GraphCompiler(self, db)

    def clone(self):
        obj = self.__class__(self.model)
        obj.filters = self.filters.copy()
        obj.relations = copy.copy(self.relations)
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
        script = GRAPH.client.scripts.get("query")
        params = self.get_query_params(count=True)
        number = GRAPH.client.gremlin(script, params).content
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

    def get_query_params(self, count=False):
        props = self.model._properties
        filters = []
        relations = copy.copy(self.relations)

        # TODO: Order by params
        order_by = []
        
        for key, value in self.filters.items():

            # turn datetime instances into bulbs-acceptable timestamps
            if isinstance(value, datetime.datetime):
                value = to_timestamp(value)
            elif isinstance(value, datetime.date):
                value = to_timestamp(datetime.datetime.combine(value, datetime.time()))

            lookup_type = "exact"
            parts = key.split(LOOKUP_SEP)
            if len(parts) > 1 and parts[-1] in OPS:
                lookup_type = parts[-1]
            if parts[0] in props or parts[0] == "eid":
                filters.append((parts[0], lookup_type, value))
            elif parts[0] in self.model._relations:
                rel = self.model._relations[parts[0]]
                relations.append((rel.relation.label, value.eid))
            else:
                raise Exception("Invalid filter lookup %s=%s for model '%s'" % (
                    key, value, self.model))

        return dict(docount=count, index_name=self.model.element_type,
                filters=filters, order_by=order_by,
                low=self.low_mark, high=self.high_mark,
                relations=relations)

    def __iter__(self):
        for iter in self.get_compiler(self.db).results_iter():
            yield iter


class GraphQuerySet(QuerySet):
    """Fake QuerySet-like class that mimics (very badly
    at the moment) the Django one."""
    def __init__(self, *args, **kwargs):
        super(GraphQuerySet, self).__init__(*args, **kwargs)
        self.query = kwargs.get("query", GraphQuery(self.model))

    def iterator(self):
        for res in self.query:
            yield res

    def values(self, *fields):
        return self._clone(klass=ValuesGraphQuerySet, setup=True, _fields=fields)

    def values_list(self, *fields, **kwargs):
        flat = kwargs.pop('flat', False)
        if kwargs:
            raise TypeError('Unexpected keyword arguments to values_list: %s'
                    % (kwargs.keys(),))
        if flat and len(fields) > 1:
            raise TypeError("'flat' is not valid when values_list is called with more than one field.")
        return self._clone(klass=ValuesListGraphQuerySet, setup=True, flat=flat,
                _fields=fields)
        
    def filter(self, **kwargs):
        clone = self._clone()
        for key, value in kwargs.items():
            clone.query = clone.query.add_filter(key, value)
        return clone

    def count(self):
        return self.query.get_count()

    def create(self, **kwargs):
        """
        Creates a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        self._for_write = True
        new_model = self.model(**kwargs)
        new_model.save()
        return new_model

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


class ValuesGraphQuerySet(GraphQuerySet):
    """Return an iterable list of value dictionaries instead of objects."""
    def iterator(self):
        for res in self.query.get_compiler(self.db).results_iter():
            yield res.to_dict()

    def _clone(self, klass=None, setup=False, **kwargs):
        """
        Cloning a ValuesQuerySet preserves the current fields.
        """
        c = super(ValuesGraphQuerySet, self)._clone(klass, **kwargs)
        if not hasattr(c, '_fields'):
            # Only clone self._fields if _fields wasn't passed into the cloning
            # call directly.
            c._fields = self._fields[:]
        c.field_names = self.field_names
        c.extra_names = self.extra_names
        c.aggregate_names = self.aggregate_names
        if setup and hasattr(c, '_setup_query'):
            c._setup_query()
        return c


    def _setup_query(self):
        """
        Constructs the field_names list that the values query will be
        retrieving.

        Called by the _clone() method after initializing the rest of the
        instance.
        """
        self.query.clear_deferred_loading()
        self.query.clear_select_fields()

        if self._fields:
            self.extra_names = []
            self.aggregate_names = []
            if not self.query.extra and not self.query.aggregates:
                # Short cut - if there are no extra or aggregates, then
                # the values() clause must be just field names.
                self.field_names = list(self._fields)
            else:
                self.query.default_cols = False
                self.field_names = []
                for f in self._fields:
                    # we inspect the full extra_select list since we might
                    # be adding back an extra select item that we hadn't
                    # had selected previously.
                    if f in self.query.extra:
                        self.extra_names.append(f)
                    elif f in self.query.aggregate_select:
                        self.aggregate_names.append(f)
                    else:
                        self.field_names.append(f)
        else:
            # Default to all fields.
            self.extra_names = None
            self.field_names = [f.attname for f in self.model._meta.fields]
            self.aggregate_names = None

        self.query.select = []
        if self.extra_names is not None:
            self.query.set_extra_mask(self.extra_names)
        self.query.add_fields(self.field_names, True)
        if self.aggregate_names is not None:
            self.query.set_aggregate_mask(self.aggregate_names)


class ValuesListGraphQuerySet(GraphQuerySet):
    """Return an iterable list of values instead of objects."""
    def iterator(self):
        for res in self.query.get_compiler(self.db).results_iter():
            # FIXME: Yield dynamic values doesn't seem to work
            yield res.eid
            #if self.flat and len(self._fields) == 1:
            #    yield getattr(res, self._fields[0], None)
            #else:
            #    yield tuple(getattr(res, f, None) for f in self._fields)

