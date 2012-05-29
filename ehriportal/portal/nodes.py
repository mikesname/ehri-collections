"""Portal model classes."""

import os
import re
import datetime
import json

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str, force_unicode

from portal import utils

import neo4django
from neo4django.db import models as neomodels


def get_unique_slug(cls, name):
    
    initial = 2
    base = slugify(name)
    potential = base
    while True:
        ires = cls.objects.filter(slug=potential)
        if len(ires) == 0:
            return potential
        potential = u"%s-%d" % (base, initial)
        initial += 1


# A note on Proxy models.
# Quite a lot of the time in this app we use 'Proxy' models that
# provide a simplified interface to a given entity. For example,
# the OtherName entity has the `type` field which tells us that
# it is (for instance) either an `other` form of name or a
# `parallel` form of name. Creating a proxy model called
# ParallelFormOfName that always sets type=`parallel` behind the
# scenes simplifies the code that uses it quite a lot. This is
# especially true when dealing with the Property class, and with
# types of reference such as NameAccess and PlaceAccess.
# The two functions below abstract the boilerplate from creating
# proxy classes that have a specific attribute with a particular
# fixed value.
def proxymanager_factory(proxymanagername, managercls, attrname):
    """Type factory for proxy managers."""
    def init_func(self, *args, **kwargs):
        setattr(self, attrname, kwargs.pop("filter_%s" % attrname, None))
        managercls.__init__(self, *args, **kwargs)

    def get_query_set_func(self, *args, **kwargs):
        qs = managercls.get_query_set(self, *args, **kwargs)
        attr = getattr(self, attrname)
        if attr is not None:
            qs = qs.filter(**{attrname:attr})
        return qs
    return type(proxymanagername, (managercls,),
            dict(__init__=init_func, get_query_set=get_query_set_func))


def proxymodel_factory(proxyname, modelcls, managercls, attrname, attrval):
    """Type factory for proxy models."""
    def save_func(self, *args, **kwargs):
        setattr(self, attrname, attrval)
        modelcls.save(self, *args, **kwargs)
    class Meta_cls:
        proxy = True
    return type(proxyname, (modelcls,),
            dict(save=save_func, Meta=Meta_cls,
                __module__=modelcls.__module__,
                __doc__="Proxy model for %s where `%s`='%s'." % (
                    modelcls.__name__, attrname, attrval),
                objects=managercls(**{"filter_%s" % attrname: attrval})))


class EntityUrlMixin(object):
    """Mixin for entity models  that have a slug and use
    revision control."""
    @models.permalink
    def get_absolute_url(self):
        return (self._meta.verbose_name + '_detail', [self.slug])

    @models.permalink
    def get_edit_url(self):
        return (self._meta.verbose_name + '_edit', [self.slug])

    @models.permalink
    def get_delete_url(self):
        return (self._meta.verbose_name + '_delete', [self.slug])

    @models.permalink
    def get_revision_url(self, version_id):
        return (self._meta.verbose_name + '_revision', [self.slug, version_id])

    @models.permalink
    def get_restore_url(self, version_id):
        return (self._meta.verbose_name + '_restore', [self.slug, version_id])

    @models.permalink
    def get_diff_url(self):
        return (self._meta.verbose_name + '_diff', [self.slug])

    @models.permalink
    def get_history_url(self):
        return (self._meta.verbose_name + '_history', [self.slug])




class ResourceNodeType(neomodels.base.NeoModelBase):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate neomodels.StringProperty attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ResourceNodeType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, vname, help in attrs.get("translatable_fields", []):
            attrs[fname] = neomodels.StringProperty(vname, null=True, blank=True, help_text=help)
        return new(cls, name, bases, attrs)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class ResourceNode(neomodels.NodeModel):
    """Archival resource."""
    __metaclass__ = ResourceNodeType
    translatable_fields = ()

    DRAFT, PUBLISHED = range(2)
    PUB_STATUS = (
            (DRAFT, _("Draft")),
            (PUBLISHED, _("Published")),
    )

    type = neomodels.StringProperty(editable=False, max_length=255)
    publication_status = neomodels.IntegerProperty(default=DRAFT, choices=PUB_STATUS)
    created_on = neomodels.DateTimeProperty(editable=False)
    updated_on = neomodels.DateTimeProperty(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(type(self), self.name)
        if not self.pk:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        if not self.type:
            self.type = self.__class__.__name__
        super(ResourceNode, self).save(*args, **kwargs)

    def get_instance(self):
        """Get the superclass instance to which this resource
        entry belongs."""
        return globals()[self.type].objects.get(pk=self.pk)

    @property
    def resource_type(self):
        return self._meta.verbose_name

    @property
    def other_names(self):
        """Get a list of other names."""
        return [on.name for on in self.othername_set.all()]

    @property
    def published(self):
        return self.publication_status == self.PUBLISHED

    @property
    def publication_status_name(self):
        return self.PUB_STATUS[self.publication_status][1]

    #def __repr__(self):
    #    return u"<%s: %d>" % (self.type, self.pk)

    #def __str__(self):
    #    if hasattr(self, '__unicode__'):
    #        return force_unicode(self).encode('utf-8')
    #    return '%s object' % self.__class__.__name__

    #def __unicode__(self):
    #    return u'<%s: %d>' % (self.__class__.__name__, self.pk)


OtherNameManager = proxymanager_factory("OtherNameManager",
        neomodels.manager.NodeModelManager, "type")


class OtherName(neomodels.NodeModel):
    OTHER, PARALLEL = range(2)
    TYPES = (
            (OTHER, _("Other")),
            (PARALLEL, "Parallel"),
    )
    name = neomodels.StringProperty(max_length=255)
    type = neomodels.IntegerProperty(choices=TYPES)
    resource = neomodels.Relationship(ResourceNode,
            rel_type=neo4django.Incoming.OWNS,
            single=True,
            related_name="othername_set")
    objects = OtherNameManager()


OtherFormOfName = proxymodel_factory("OtherFormOfName",
        OtherName, OtherNameManager, "type", OtherName.OTHER)
ParallelFormOfName = proxymodel_factory("ParallelFormOfName",
        OtherName, OtherNameManager, "type", OtherName.PARALLEL)



class RepositoryNodeManager(neomodels.manager.NodeModelManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class RepositoryNode(ResourceNode, EntityUrlMixin):
    """RepositoryNode."""
    ENTITY_TYPES=()
    LODS = ()

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

    name = neomodels.StringProperty(indexed=True, max_length=255)
    slug = neomodels.StringProperty(indexed=True, 
            unique=True, max_length=255, editable=False)
    identifier = neomodels.StringProperty(indexed=True, unique=True, max_length=255)
    lod = neomodels.StringProperty(max_length=255, choices=LODS, blank=True, null=True)
    type_of_entity = neomodels.StringProperty(max_length=255,
            choices=ENTITY_TYPES, blank=True, null=True)
    languages = neomodels.StringArrayProperty(blank=True)
    scripts = neomodels.StringArrayProperty(blank=True)
    objects = RepositoryNodeManager()

    class Meta:
        verbose_name_plural = "repositories"

    def natural_key(self):
        return (self.slug,)

    @property
    def primary_contact(self):
        """Get the main contact property."""
        try:
            return self.contact_set.all().order_by("primary")[0]
        except IndexError:
            return None

    @property
    def country_code(self):
        contact = self.primary_contact
        if contact:
            return contact.country_code

    @property
    def country(self):
        contact = self.primary_contact
        if contact and contact.country_code:
            return utils.country_name_from_code(contact.country_code)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)

    def __unicode__(self):
        return self.name


class Contact(neomodels.NodeModel):
    """Contact class."""
    CONTACT_TYPES = ()

    primary = models.BooleanField(_("Primary Contact"))
    repository = neomodels.Relationship(RepositoryNode, rel_type=neo4django.Incoming.OWNS,
                single=True, related_name="contact_set")
    contact_person = neomodels.StringProperty(max_length=255, null=True, blank=True)
    street_address = neomodels.StringProperty(null=True, blank=True)
    city = neomodels.StringProperty(max_length=100, null=True, blank=True)
    region = neomodels.StringProperty(max_length=100, null=True, blank=True)
    postal_code = neomodels.StringProperty(max_length=100, null=True, blank=True)
    country_code = neomodels.StringProperty(max_length=100, null=True, blank=True,
            choices=utils.country_choices())
    website = neomodels.URLProperty(null=True, blank=True)
    email = neomodels.EmailProperty(null=True, blank=True)
    telephone = neomodels.StringProperty(max_length=100, null=True, blank=True)
    fax = neomodels.StringProperty(max_length=100, null=True, blank=True)
    contact_type = neomodels.StringProperty(max_length=100, blank=True,
                null=True, choices=CONTACT_TYPES)
    note = neomodels.StringProperty(null=True, blank=True)
    created_on = neomodels.DateTimeProperty(editable=False)
    updated_on = neomodels.DateTimeProperty(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Contact, self).save(*args, **kwargs)

    def coordinates(self):
        """Get coords as a tuple."""
        return self.latitude, self.longitude

    def format(self):
        elems = [e.strip() for e in [
            self.street_address,
            self.postal_code,
            self.city,
            self.region,
            utils.country_name_from_code(self.country_code) \
                    if self.country_code else None
        ] if e is not None]
        return "\n".join(elems).replace(", ", "\n")


class CollectionManager(neomodels.manager.NodeModelManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Collection(ResourceNode, EntityUrlMixin):
    """Model representing an archival description."""
    COLLECTION, FONDS, SUBFONDS, SERIES, SUBSERIES, FILE, ITEM = range(7)
    LODS = (
        (COLLECTION, _("Collection")),
        (FONDS, _("Fonds")),
        (SUBFONDS, _("Sub-fonds")),
        (SERIES, _("Series")),
        (SUBSERIES, _("Sub-series")),
        (FILE, _("File")),
        (ITEM, _("Item")),
    )

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

    name = neomodels.StringProperty(max_length=255)
    slug = neomodels.StringProperty(indexed=True, max_length=255,
                unique=True, editable=False)
    identifier = neomodels.StringProperty(max_length=255)
    lod = neomodels.IntegerProperty(choices=LODS,
                blank=True, null=True)
    creator = neomodels.Relationship("Authority", rel_type=neo4django.Incoming.OWNS,
                single=True, related_name="collection_set", optional=True)
    repository = neomodels.Relationship(RepositoryNode, rel_type=neo4django.Incoming.OWNS,
                single=True, related_name="collection_set")
    languages = neomodels.StringArrayProperty(blank=True)
    scripts = neomodels.StringArrayProperty(blank=True)
    languages_of_description = neomodels.StringArrayProperty(
                _("Language(s) of Description"), blank=True)
    scripts_of_description = neomodels.StringArrayProperty(
                _("Script(s) of Description"), blank=True)

    objects = CollectionManager()

    class Meta:
        verbose_name_plural = "collections"
        unique_together = (("identifier", "repository"),)

    def natural_key(self):
        return (self.slug,)

    @property
    def start_date(self):
        """Shortcut for getting the earliest date to which
        this collection relates."""
        try:
            fdate = self.date_set.all().order_by("start_date")[0]
        except IndexError:
            return
        return fdate.start_date

    @property
    def end_date(self):
        """Shortcut for getting the lastest date to which
        this collection relates."""
        try:
            edate = self.date_set.all().order_by("-end_date", "-start_date")[0]
        except IndexError:
            return
        if edate.end_date:
            return edate.end_date
        return edate.start_date

    @property
    def date(self):
        """Average of start/end dates. Not exact."""
        if not self.end_date and not self.start_date:
            return
        if not self.end_date:
            return self.start_date
        return self.start_date + ((self.end_date - self.start_date) / 2)

    @property
    def date_range(self):
        """List of years this collection covers."""
        if not self.end_date and not self.start_date:
            return []
        if not self.end_date:
            return [self.start_date]
        return [datetime.date(y,1,1) for y in \
                range(self.start_date.year, self.end_date.year + 1)]

    @property
    def date_range_string(self):
        """List of years this collection covers."""
        dates = self.date_range
        if not dates:
            return None
        if len(dates) == 1:
            return str(self.start_date.year)
        return "%s-%s" % (dates[0].year, dates[-1].year)

    @property
    def name_access(self):
        # TODO: Find the proper way of doing this
        return [ne.subject for ne in NameAccess.objects.select_related()\
                    .filter(object_id=self.id).all()]

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)

    def __unicode__(self):
        return self.name


AuthorityManager = proxymanager_factory("AuthorityManager",
        neomodels.manager.NodeModelManager, "type_of_entity")
AuthorityManager.get_by_natural_key = lambda self, slug: self.get(slug=slug)


class Authority(ResourceNode, EntityUrlMixin):
    """Model representing an archival authority."""
    FULL, PARTIAL, MINIMAL = range(3)
    CORP, FAMILY, PERSON = range(3)

    LODS = (
        (FULL, _("Full")),
        (PARTIAL, _("Partial")),
        (MINIMAL, _("Minimal")),
    )
    ENTITY_TYPES = (
        (CORP, _("Corporate Body")),
        (FAMILY, _("Family")),
        (PERSON, _("Person")),
    )

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

    name = neomodels.StringProperty(max_length=255)
    slug = neomodels.StringProperty(indexed=True, max_length=255,
                unique=True, editable=False)
    identifier = neomodels.StringProperty(max_length=255)
    lod = models.PositiveIntegerField(choices=LODS, blank=True, null=True)
    type_of_entity = neomodels.IntegerProperty(choices=ENTITY_TYPES, blank=True, null=True)
    languages = neomodels.StringArrayProperty(blank=True)
    scripts = neomodels.StringArrayProperty(blank=True)
    objects = AuthorityManager()

    class Meta:
        verbose_name_plural = "authorities"

    def natural_key(self):
        return (self.slug,)

    @property
    def type_name(self):
        return self.ENTITY_TYPES[self.type_of_entity][1]

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)

    def __unicode__(self):
        return self.name

# Proxy models for different types of authority
Person = proxymodel_factory("Person", Authority, AuthorityManager,
        "type_of_entity", Authority.PERSON)
Family = proxymodel_factory("Family", Authority, AuthorityManager,
        "type_of_entity", Authority.FAMILY)
CorporateBody = proxymodel_factory("CorporateBody", Authority, AuthorityManager,
        "type_of_entity", Authority.CORP)


class FuzzyDate(neomodels.NodeModel):
    """Model representing an approximate historical
    date or a date range."""
    CHOICES = (
            ("year", "Year"),
            ("month", "Month"),
            ("day", "Day"),
    )
    collection = neomodels.Relationship(Collection, rel_type=neo4django.Incoming.OWNS,
            single=True, related_name="date_set")
    start_date = neomodels.DateProperty()
    #start_time = models.TimeField(blank=True, null=True)
    end_date = neomodels.DateProperty(blank=True, null=True)
    #end_time = models.TimeField(blank=True, null=True)
    precision = neomodels.StringProperty(max_length=20, choices=CHOICES)
    #circa = models.BooleanField(default=False)

    @classmethod
    def from_fuzzy_date(cls, datestr):
        """Parse dates like "1939-1946", "c 1945" etc. This exists solely
        for importing dates from Aim25 web scrapes, and will go away some
        point in the future."""
        m1 = re.search("^(?P<start>\d{4})\s*-\s*(?P<end>\d{4})(?P<ish>s)?$", datestr.strip())
        fdate = FuzzyDate()
        if m1:
            d1 = datetime.date(int(m1.group("start")), 1, 1)
            d2 = datetime.date(int(m1.group("end")), 12, 31)
            fdate.start_date = d1
            fdate.end_date = d2
            fdate.circa = m1.group("ish") is not None
            fdate.precision = "year"
            return fdate
        m2 = re.search("^(?P<circa>c)?\s?(?P<year>\d{4})$", datestr.strip())
        if m2:
            d1 = datetime.date(int(m2.group("year")), 1, 1)
            fdate.start_date = d1
            fdate.circa = m2.group("circa") is not None
            fdate.precision = "year"
            return fdate
        # fallback - try and parse with dateutil...
        try:
            from dateutil import parser
            fdate.start_date = parser.parse(datestr, default=datetime.date(2012, 1, 1))
            return fdate
        except (ValueError, TypeError):
            return None

    def __unicode__(self):
        """Print a sensible representation."""
        out = ""
        if self.circa:
            out += "c"
        # TODO: Make this format properly
        out += str(self.start_date.year)
        if self.end_date:
            out += "-%d" % self.end_date.year
        return out


