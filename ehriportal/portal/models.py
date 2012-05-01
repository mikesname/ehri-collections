"""Portal model classes."""

import os
import re
import datetime
import json

from django.contrib.gis.db import models
from django.db.models.base import ModelBase
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from autoslug import AutoSlugField
import jsonfield

from portal import utils
from portal.thumbs import ImageWithThumbsField

import reversion

from south.modelsinspector import add_introspection_rules

EMPTY_JSON_LIST = json.dumps([])

# get South to play nice with ImageWithThumbsField
add_introspection_rules(
    [
        (
            (ImageWithThumbsField, ),
            [],
            {
                "verbose_name": ["verbose_name", {"default": None}],
                "name":         ["name",         {"default": None}],
                "width_field":  ["width_field",  {"default": None}],
                "height_field": ["height_field", {"default": None}],
                "sizes":        ["sizes",        {"default": None}],
            },
        ),
    ],
    ["^portal\.thumbs\.ImageWithThumbsField",]
)


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




class ResourceType(ModelBase):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, vname, help in attrs.get("translatable_fields", []):
            attrs[fname] = models.TextField(vname, null=True, blank=True, help_text=help)
        return new(cls, name, bases, attrs)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class Resource(models.Model):
    """Archival resource."""
    __metaclass__ = ResourceType
    translatable_fields = ()

    type = models.CharField(editable=False, max_length=255)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        if not self.type:
            self.type = self.__class__.__name__
        super(Resource, self).save(*args, **kwargs)

    def get_instance(self):
        """Get the superclass instance to which this resource
        entry belongs."""
        return globals()[self.type].objects.get(pk=self.pk)

    @property
    def other_names(self):
        """Get a list of other names."""
        return [on.name for on in self.othername_set.all()]

    @property
    def images(self):
        """Shortcut for fetching associated images."""
        return self.resourceimage_set.all()

    @property
    def properties(self):
        """Get a list of property key/value pairs."""
        return [(p.name, p.value) for p in self.property_set.all()]

    @property
    def tag_list(self):
        """Short cut for listing all tags."""
        return self.tags.all()

    def get_property(self, propname):
        """Fetch a list of properties with the given name."""
        return [p[1] for p in self.properties if p[0] == propname]

    def set_property(self, name, value):
        """Set a property.  This does NOT imply overwriting
        existing ones, since multiple properties can have the
        same name, i.e. language: [en, de]."""
        prop, created = Property.objects.get_or_create(
                    resource=self, name=name, value=value)

    def delete_property(self, name, withval=None):
        """Delete a property with the given name and (optionally)
        the given value."""
        qset = self.property_set.filter(name=name)
        if withval is not None:
            qset = self.property_set.filter(value=value)
        qset.delete()

    def __repr__(self):
        return u"<%s: %d>" % (self.type, self.pk)

reversion.register(Resource, follow=[
        "property_set", "place_set", "othername_set", "resourceimage_set"])


class ResourceImage(models.Model):
    """Images associated with resources."""
    resource = models.ForeignKey(Resource)
    image = ImageWithThumbsField(
            upload_to=lambda inst, fn: os.path.join(inst.resource.slug,
                "%s%s" % (inst.resource.slug,
                    os.path.splitext(fn)[1])), sizes=settings.THUMBNAIL_SIZES)
    caption = models.CharField(max_length=255, null=True, blank=True)
reversion.register(ResourceImage)


OtherNameManager = proxymanager_factory("OtherNameManager",
        models.Manager, "type")


class OtherName(models.Model):
    OTHER, PARALLEL = range(2)
    TYPES = (
            (OTHER, _("Other")),
            (PARALLEL, "Parallel"),
    )
    name = models.CharField("Alternate name", max_length=255)
    type = models.PositiveIntegerField(_("Type of name"), choices=TYPES)
    resource = models.ForeignKey(Resource)
    objects = OtherNameManager()
reversion.register(OtherName)


OtherFormOfName = proxymodel_factory("OtherFormOfName",
        OtherName, OtherNameManager, "type", OtherName.OTHER)
ParallelFormOfName = proxymodel_factory("ParallelFormOfName",
        OtherName, OtherNameManager, "type", OtherName.PARALLEL)


RelationManager = proxymanager_factory("RelationManager",
        models.Manager, "type")


class Relation(models.Model):
    """Relationship between two objects."""
    NAME, PLACE = range(2)
    TYPES = (
            (NAME, _("Name Access")),
            (PLACE, _("Place Access")),
    )
    subject = models.ForeignKey(Resource, related_name="+")
    object = models.ForeignKey(Resource, related_name="+")
    type = models.PositiveIntegerField(_("Type of Relationship"), choices=TYPES)
    objects = RelationManager()


NameAccess = proxymodel_factory("NameAccess", Relation, RelationManager,
            "type", Relation.NAME)
PlaceAccess = proxymodel_factory("PlaceAccess", Relation, RelationManager,
            "type", Relation.PLACE)


PropertyManager = proxymanager_factory("PropertyManager",
        models.Manager, "name")


class Property(models.Model):
    """Generic property for resources."""
    resource = models.ForeignKey(Resource)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    objects = PropertyManager()
reversion.register(Property)


def propertyproxy_factory(propname):
    """Get a class that represents a property of
    a specific given name, i.e. script or language."""
    return proxymodel_factory("Property_%s" % propname, Property,
            PropertyManager, "name", propname)


class Place(models.Model):
    """A point on the earth associated with a resource."""
    resource = models.ForeignKey(Resource)
    point = models.PointField()
    objects = models.GeoManager()
reversion.register(Place)


class RepositoryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Repository(Resource, EntityUrlMixin):
    """Repository."""
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

    name = models.CharField("Authorized Form of Name", max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    identifier = models.CharField(max_length=255)
    lod = models.CharField("Level of Description", max_length=255, choices=LODS, blank=True, null=True)
    type_of_entity = models.CharField("Type of Entity", max_length=255,
            choices=ENTITY_TYPES, blank=True, null=True)
    logo = ImageWithThumbsField("Logo", null=True, blank=True,
            upload_to=lambda inst, fn: os.path.join(inst.slug,
                "%s_logo%s" % (inst.slug,
                    os.path.splitext(fn)[1])), sizes=settings.THUMBNAIL_SIZES)
    languages = jsonfield.JSONField(_("Language(s)"), blank=True, default=EMPTY_JSON_LIST)
    scripts = jsonfield.JSONField(_("Script(s)"), blank=True, default=EMPTY_JSON_LIST)
    tags = TaggableManager(blank=True)
    objects = RepositoryManager()

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
reversion.register(Repository, follow=["resource_ptr", "contact_set"])


class Contact(models.Model):
    """Contact class."""
    CONTACT_TYPES = ()

    primary = models.BooleanField(_("Primary Contact"))
    repository = models.ForeignKey(Repository, verbose_name="Contact addresses")
    contact_person = models.CharField(_("Contact Person"), max_length=255, null=True, blank=True)
    street_address = models.TextField(_("Street Address"), null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    region = models.CharField(_("Region"), max_length=100, null=True, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=100, null=True, blank=True)
    country_code = models.CharField(_("Country"), max_length=100, null=True, blank=True,
            choices=utils.country_choices())
    website = models.URLField(_("Website"), null=True, blank=True)
    email = models.EmailField(_("Email"), null=True, blank=True)
    telephone = models.CharField(_("Telephone"), max_length=100, null=True, blank=True)
    fax = models.CharField(_("Fax"), max_length=100, null=True, blank=True)
    contact_type = models.CharField(_("Contact Type"),
            max_length=100, blank=True, null=True, choices=CONTACT_TYPES)
    note = models.TextField(_("Notes"), null=True, blank=True)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

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
reversion.register(Contact)


class CollectionManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Collection(Resource, EntityUrlMixin):
    """Model representing an archival description."""
    COLLECTION, FONDS = range(2)
    LODS = (
        (FONDS, _("Fonds")),
        (COLLECTION, _("Collection")),
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
        ("physical_characteristics", "Physical Characteristics", "TODO: Help text"),
        ("related_units_of_description", "Related Units of Description", "TODO: Help text"),
        ("reproduction_conditions", "Reproduction Conditions", "TODO: Help text"),
        ("revision_history", "Revision History", "TODO: Help text"),
        ("rules", "Rules", "TODO: Help text"),
        ("scope_and_content", "Scope and Content", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    name = models.CharField("Title", max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    identifier = models.CharField(max_length=255)
    lod = models.PositiveIntegerField(_("Level of Description"), choices=LODS,
                blank=True, null=True)
    creator = models.ForeignKey("Authority", null=True, blank=True)
    repository = models.ForeignKey(Repository)
    languages = jsonfield.JSONField(_("Language(s) of Materials"), blank=True, default=EMPTY_JSON_LIST)
    scripts = jsonfield.JSONField(_("Script(s) of Materials"), blank=True, default=EMPTY_JSON_LIST)
    languages_of_description = jsonfield.JSONField(
                _("Language(s) of Description"), blank=True, default=EMPTY_JSON_LIST)
    scripts_of_description = jsonfield.JSONField(
                _("Script(s) of Description"), blank=True, default=EMPTY_JSON_LIST)

    tags = TaggableManager(blank=True)
    objects = CollectionManager()

    class Meta:
        verbose_name_plural = "collections"

    def natural_key(self):
        return (self.slug,)

    @property
    def name_access(self):
        # TODO: Find the proper way of doing this
        return [ne.subject for ne in NameAccess.objects.select_related()\
                    .filter(object=self).all()]

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

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)

    def __unicode__(self):
        return self.name
reversion.register(Collection, follow=["resource_ptr", "date_set"])


AuthorityManager = proxymanager_factory("AuthorityManager",
        models.Manager, "type_of_entity")
AuthorityManager.get_by_natural_key = lambda self, slug: self.get(slug=slug)


class Authority(Resource, EntityUrlMixin):
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

    name = models.CharField("Authorized Form of Name", max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    identifier = models.CharField(max_length=255)
    lod = models.PositiveIntegerField(_("Level of Description"), choices=LODS,
                blank=True, null=True)
    type_of_entity = models.PositiveIntegerField(_("Type of Entity"),
            choices=ENTITY_TYPES, blank=True, null=True)
    languages = jsonfield.JSONField(_("Language(s)"), blank=True, default=EMPTY_JSON_LIST)
    scripts = jsonfield.JSONField(_("Script(s)"), blank=True, default=EMPTY_JSON_LIST)
    tags = TaggableManager(blank=True)
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
reversion.register(Authority, follow=[
        "resource_ptr", "property_set", "place_set"])

# Proxy models for different types of authority
Person = proxymodel_factory("Person", Authority, AuthorityManager,
        "type_of_entity", Authority.PERSON)
Family = proxymodel_factory("Family", Authority, AuthorityManager,
        "type_of_entity", Authority.FAMILY)
CorporateBody = proxymodel_factory("CorporateBody", Authority, AuthorityManager,
        "type_of_entity", Authority.CORP)


class FuzzyDate(models.Model):
    """Model representing an approximate historical
    date or a date range."""
    CHOICES = (
            ("year", "Year"),
            ("month", "Month"),
            ("day", "Day"),
    )
    collection = models.ForeignKey(Collection, related_name="date_set")
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    precision = models.CharField(max_length=20, choices=CHOICES)
    circa = models.BooleanField(default=False)

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
reversion.register(FuzzyDate)

