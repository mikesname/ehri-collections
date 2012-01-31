"""Portal model classes."""

import re
import datetime
import calendar

from django.db import models
from django.db.models.base import ModelBase

from taggit.managers import TaggableManager
from autoslug import AutoSlugField

from ehriportal.portal import utils

class ResourceType(ModelBase):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, help in attrs.get("translatable_fields", []):
            attrs[fname] = models.TextField(null=True, blank=True, help_text=help)
        return new(cls, name, bases, attrs)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class Resource(models.Model):
    """Archival resource."""
    __metaclass__ = ResourceType
    translatable_fields = ()

    ENTITY_TYPES=()
    LOD = ()

    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    type = models.CharField(max_length=255)
    lod = models.CharField(max_length=255, choices=LOD, blank=True, null=True)
    type_of_entity = models.CharField(max_length=255,
            choices=ENTITY_TYPES, blank=True, null=True)
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

    @property
    def other_names(self):
        """Get a list of other names."""
        return [on.name for on in self.othername_set.all()]

    @property
    def properties(self):
        """Get a list of property key/value pairs."""
        return [(p.name, p.value) for p in self.property_set.all()]

    @property
    def languages(self):
        """Short cut for fetching language properties."""
        return self.get_property("language")

    @property
    def tag_list(self):
        """Short cut for listing all tags."""
        return self.tags.all()

    @property
    def scripts(self):
        """Short cut for fetching language properties."""
        return self.get_property("script")

    def get_property(self, propname):
        """Fetch a list of properties with the given name."""
        return [p[1] for p in self.properties if p[0] == propname]

    def set_property(self, name, value):
        """Set a property.  This does NOT imply overwriting 
        existing ones, since multiple properties can have the
        same name, i.e. language: [en, de]."""
        self.property_set.add(Property(resource=self, name=name, value=value))

    def delete_property(self, name, withval=None):
        """Delete a property with the given name and (optionally)
        the given value."""
        qset = self.property_set.filter(name=name)
        if withval is not None:
            qset = self.property_set.filter(value=value)
        qset.delete()

    def __unicode__(self):
        return u"<%s: %s>" % (self.type, self.identifier)


class OtherName(models.Model):
    name = models.CharField(max_length=255)
    resource = models.ForeignKey(Resource)


class Property(models.Model):
    """Generic property for resources."""
    resource = models.ForeignKey(Resource)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Repository(Resource):
    """Repository."""
    ENTITY_TYPES=()
    LOD = ()

    translatable_fields = (
        ("access_conditions", "TODO: Help text"),
        ("buildings", "TODO: Help text"),
        ("collecting_policies", "TODO: Help text"),
        ("dates_of_existence", "TODO: Help text"),
        ("disabled_access", "TODO: Help text"),
        ("finding_aids", "TODO: Help text"),
        ("functions", "TODO: Help text"),
        ("general_context", "TODO: Help text"),
        ("geocultural_context", "TODO: Help text"),
        ("history", "TODO: Help text"),
        ("holdings", "TODO: Help text"),
        ("internal_structures", "TODO: Help text"),
        ("legal_status", "TODO: Help text"),
        ("maintenance_notes", "TODO: Help text"),
        ("mandates", "TODO: Help text"),
        ("opening_times", "TODO: Help text"),
        ("places", "TODO: Help text"),
        ("reproduction_services", "TODO: Help text"),
        ("research_services", "TODO: Help text"),
        ("rules", "TODO: Help text"),
        ("sources", "TODO: Help text"),
    )

    image = models.ImageField(null=True, blank=True,
            upload_to=lambda inst, fn: "%s%s" % (inst.slug,
                    os.path.splitext(fn)[1]))

    tags = TaggableManager()

    class Meta:
        verbose_name_plural = "repositories"

    @property
    def primary_contact(self):
        """Get the main contact property."""
        try:
            return self.contacts.all().order_by("primary")[0]
        except IndexError:
            return None

    @property
    def country(self):
        contact = self.primary_contact
        if contact is None:
            return
        return utils.get_country_from_code(contact.country_code)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('repo_detail', [self.slug])


class Contact(models.Model):
    """Contact class."""
    CONTACT_TYPES = ()

    primary = models.BooleanField()
    repository = models.ForeignKey(Repository, related_name="contacts")
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    fax = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    contact_type = models.CharField(
            max_length=100, blank=True, null=True, choices=CONTACT_TYPES)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Contact, self).save(*args, **kwargs)

    def format(self):
        elems = [e.strip() for e in [
            self.street_address,
            self.postal_code,
            self.city,
            self.region,
            utils.get_country_from_code(self.country_code)
        ] if e is not None]
        return "\n".join(elems).replace(", ", "\n")


class Collection(Resource):
    """Model representing an archival description."""
    LODS = (
        ("fonds", "Fonds"),
        ("collection", "Collection"),
    )
    ENTITY_TYPES = ()

    translatable_fields = (
        ("access_conditions", "TODO: Help text"),
        ("accruals", "TODO: Help text"),
        ("acquisition", "TODO: Help text"),
        ("alternate_title", "TODO: Help text"),
        ("appraisal", "TODO: Help text"),
        ("archival_history", "TODO: Help text"),
        ("arrangement", "TODO: Help text"),
        ("edition", "TODO: Help text"),
        ("extent_and_medium", "TODO: Help text"),
        ("finding_aids", "TODO: Help text"),
        ("institution_responsible_identifier", "TODO: Help text"),
        ("location_of_copies", "TODO: Help text"),
        ("location_of_originals", "TODO: Help text"),
        ("physical_characteristics", "TODO: Help text"),
        ("related_units_of_description", "TODO: Help text"),
        ("reproduction_conditions", "TODO: Help text"),
        ("revision_history", "TODO: Help text"),
        ("rules", "TODO: Help text"),
        ("scope_and_content", "TODO: Help text"),
        ("sources", "TODO: Help text"),
    )

    repository = models.ForeignKey(Repository)

    tags = TaggableManager()

    class Meta:
        verbose_name_plural = "collections"

    @property
    def languages_of_description(self):
        return self.get_property("languages_of_description")

    @property
    def start_date(self):
        """Shortcut for getting the earliest date to which
        this collection relates."""
        try:
            fdate = self.dates.all().order_by("start_date")[0]
        except IndexError:
            return
        return fdate.start_date

    @property
    def end_date(self):
        """Shortcut for getting the lastest date to which
        this collection relates."""
        try:
            edate = self.dates.all().order_by("-end_date", "-start_date")[0]
        except IndexError:
            return
        if edate.end_date:
            return edate.end_date
        return edate.start_date

    @models.permalink
    def get_absolute_url(self):
        return ('collection_detail', [self.slug])


class FuzzyDate(models.Model):
    """Model representing an approximate historical
    date or a date range."""
    CHOICES = (
            ("year", "Year"),
            ("month", "Month"),
            ("day", "Day"),
    )
    collection = models.ForeignKey(Collection, related_name="dates")
    start_date = models.DateField()
    start_time = models.TimeField(null=True)    
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)
    precision = models.CharField(max_length=20, choices=CHOICES)
    circa = models.BooleanField(default=False)

    @classmethod
    def from_fuzzy_date(cls, datestr):
        """Parse dates like "1939-1946", "c 1945" etc. This exists solely
        for importing dates from Aim25 web scrapes, and will go away some
        point in the future."""
        m1 = re.search("^(?P<start>\d{4})-(?P<end>\d{4})(?P<ish>s)?$", datestr.strip())
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


