"""
Django Shims for Bulbs models.
"""


from django.db.models.query import QuerySet as DjangoQuerySet
from django.db.models.sql import Query as DjangoQuery
from django.db.models.sql.constants import ORDER_PATTERN

from bulbs.utils import initialize_elements

from . import graph as GRAPH

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

