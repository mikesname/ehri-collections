"""
Portal entities as Bulb Graph nodes.
"""

import os
import sys
import re
import datetime
import json
import functools

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from portal import utils, terms, models

import djbulbs
from djbulbs.models import nodeprop
from djbulbs.manager import GraphManager

current_datetime = datetime.datetime.now

class HeldBy(djbulbs.models.Relationship):
    label = "heldBy"
djbulbs.graph.add_proxy(HeldBy.label, HeldBy)


class CreatedBy(djbulbs.models.Relationship):
    label = "createdBy"
djbulbs.graph.add_proxy(CreatedBy.label, CreatedBy)


class AddressOf(djbulbs.models.Relationship):
    label = "addressOf"
djbulbs.graph.add_proxy(AddressOf.label, AddressOf)


class MentionedIn(djbulbs.models.Relationship):
    label = "mentionedIn"
djbulbs.graph.add_proxy(MentionedIn.label, MentionedIn)


class Describes(djbulbs.models.Relationship):
    label = "describes"
djbulbs.graph.add_proxy(Describes.label, Describes)


# FIXME: Think up a proper name for this relationship
class LocatesInTime(djbulbs.models.Relationship):
    label = "locatesInTime"
djbulbs.graph.add_proxy(LocatesInTime.label, LocatesInTime)


def cachedproperty(f):
    """Property constructor that memoizes the result.
    TODO: Make it possible to reset this easily..."""
    name = f.__name__
    def getter(self):
        try:
            return self.__dict__["_%s_cache" % name]
        except KeyError:
            res = self.__dict__["_%s_cache" % name] = f(self)
            return res
    return property(getter)


class ResourceBaseType(djbulbs.models.ModelType):
    """Metaclass for resource types. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        super_new = super(ResourceBaseType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        new_class = super_new(cls, name, bases, attrs)
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new_class 
        for fname, vname, help in attrs.get("translatable_fields", []):
            new_class.add_to_class(fname, nodeprop.String(name=vname, nullable=True))
        return new_class



class ResourceBase(djbulbs.models.Model, models.EntityUrlMixin):
    """Mixin for resources holding common properties."""
    __metaclass__ = ResourceBaseType
    # Publication status enum
    DRAFT, PUBLISHED = range(2)
    PUB_STATUS = (
            (DRAFT, _("Draft")),
            (PUBLISHED, _("Published")),
    )
    # FIXME: Mock attrs for testing
    other_names = []
    from django.db.models.query import EmptyQuerySet
    place_set = EmptyQuerySet()
    #languages = []
    #languages_of_description = []
    #scripts = []
    #scripts_of_description = []

    name = nodeprop.String(name=_("Name"), unique=True, indexed=True, nullable=False)
    slug = nodeprop.String(name=_("Slug"), unique=True, indexed=True, nullable=False)
    created_on = nodeprop.DateTime(name=_("Date Created"), nullable=False)
    updated_on = nodeprop.DateTime(name=_("Date Updated"), nullable=True)
    publication_status = nodeprop.Integer(name=_("Publication Status"),
            default=DRAFT, indexed=True)

    def _get_slug(self, name):
        proxy = getattr(djbulbs.graph, self.element_type)
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

    @property
    def resource_type(self):
        return self._meta.verbose_name

    @property
    def published(self):
        return self.publication_status == self.PUBLISHED

    @cachedproperty
    def tag_list(self):
        return Keyword.objects.incoming(Describes, self)

    def save(self, *args, **kwargs):
        if not hasattr(self, "eid"):
            # Grotesque hacks to get around Bulbs difficulties. Because
            # of the convoluted way that item._data gets populated, and
            # the distinction between stored and regular properties
            self._data["slug"] = self.slug = self._get_slug(self._data["name"])
            self._data["created_on"] = self.created_on = current_datetime()
        else:
            self._data["updated_on"] = self.updated_on = current_datetime()
        return super(ResourceBase, self).save(*args, **kwargs)

    def to_dict(self):
        """Serialize to dictionary."""
        return self.data()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)



class Repository(ResourceBase):
    """Repository."""
    element_type = "repository"
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"), nullable=True)
        
    access_conditions = nodeprop.String(name=_("Access Conditions"), nullable=True)
    buildings = nodeprop.String(name=_("Buildings"), nullable=True)
    collecting_policies = nodeprop.String(name=_("Collecting Policies"), nullable=True)
    dates_of_existence = nodeprop.String(name=_("Dates of Existence"), nullable=True)
    disabled_access = nodeprop.String(name=_("Disabled Access"), nullable=True)
    finding_aids = nodeprop.String(name=_("Finding Aids"), nullable=True)
    functions = nodeprop.String(name=_("Functions"), nullable=True)
    general_context = nodeprop.String(name=_("General Context"), nullable=True)
    geocultural_context = nodeprop.String(name=_("Geocultural Context"), nullable=True)
    history = nodeprop.String(name=_("History"), nullable=True)
    holdings = nodeprop.String(name=_("Holdings"), nullable=True)
    internal_structures = nodeprop.String(name=_("Internal Structures"), nullable=True)
    legal_status = nodeprop.String(name=_("Legal Status"), nullable=True)
    maintenance_notes = nodeprop.String(name=_("Maintenance Notes"), nullable=True)
    mandates = nodeprop.String(name=_("Mandates"), nullable=True)
    opening_times = nodeprop.String(name=_("Opening Times"), nullable=True)
    places = nodeprop.String(name=_("Places"), nullable=True)
    reproduction_services = nodeprop.String(name=_("Reproduction Services"), nullable=True)
    research_services = nodeprop.String(name=_("Research Services"), nullable=True)
    rules = nodeprop.String(name=_("Rules"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    @cachedproperty
    def primary_contact(self):
        try:
            # TODO: Actually pick out the primary contact!
            return Contact.objects.filter(repository=self)[0]
        except IndexError:
            pass

    @property
    def country_code(self):
        contact = self.primary_contact
        if contact:
            return contact.country_code

    @cachedproperty
    def contact_set(self):
        return Contact.objects.filter(repository=self)

    @cachedproperty
    def collection_set(self):
        return Collection.objects.filter(repository=self)

    @property
    def collections(self):
        """Get all collections related by the heldBy edge."""
        return self.collection_set.all()

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Repository.element_type, Repository)


class Collection(ResourceBase):
    """Model representing an archival description."""
    element_type = "collection"
    translatable_fields = ()

    objects = GraphManager()

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))

    access_conditions = nodeprop.String(name=_("Access Conditions"), nullable=True)
    accruals = nodeprop.String(name=_("Accruals"), nullable=True)
    acquisition = nodeprop.String(name=_("Immediate source of acquisition or transfer"), nullable=True)
    alternate_title = nodeprop.String(name=_("Alternate Title"), nullable=True)
    appraisal = nodeprop.String(name=_("Appraisal"), nullable=True)
    archival_history = nodeprop.String(name=_("Archival History"), nullable=True)
    arrangement = nodeprop.String(name=_("Arrangement"), nullable=True)
    edition = nodeprop.String(name=_("Edition"), nullable=True)
    extent_and_medium = nodeprop.String(name=_("Extent and Medium"), nullable=True)
    finding_aids = nodeprop.String(name=_("Finding Aids"), nullable=True)
    institution_responsible_identifier = nodeprop.String(name=_("Institution Responsible Identifier"), nullable=True)
    location_of_copies = nodeprop.String(name=_("Location of Copies"), nullable=True)
    location_of_originals = nodeprop.String(name=_("Location of Originals"), nullable=True)
    notes = nodeprop.String(name=_("Notes"), nullable=True)
    physical_characteristics = nodeprop.String(name=_("Physical Characteristics"), nullable=True)
    related_units_of_description = nodeprop.String(name=_("Related Units of Description"), nullable=True)
    reproduction_conditions = nodeprop.String(name=_("Reproduction Conditions"), nullable=True)
    revision_history = nodeprop.String(name=_("Revision History"), nullable=True)
    rules = nodeprop.String(name=_("Rules"), nullable=True)
    scope_and_content = nodeprop.String(name=_("Scope and Content"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))
    languages_of_description = nodeprop.List(name=_("Language(s) of Description"))
    scripts_of_description = nodeprop.List(name=_("Script(s) of Description"))

    creator = djbulbs.models.SingleRelationField(CreatedBy)
    repository = djbulbs.models.SingleRelationField(HeldBy)

    @cachedproperty
    def date_set(self):
        return FuzzyDate.objects.filter(collection=self)

    @cachedproperty
    def start_date(self):
        """Shortcut for getting the earliest date to which
        this collection relates."""
        try:
            fdate = self.date_set.all().order_by("start_date")[0]
        except IndexError:
            return
        return fdate.start_date

    @cachedproperty
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

    @cachedproperty
    def date(self):
        """Average of start/end dates. Not exact."""
        if not self.end_date and not self.start_date:
            return
        if not self.end_date:
            return self.start_date
        return self.start_date + ((self.end_date - self.start_date) / 2)

    @cachedproperty
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

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Collection.element_type, Collection)


class Contact(ResourceBase):
    """Model representing a repository's address."""
    element_type = "contact"

    primary = nodeprop.Integer(name=_("Primary Contact"))
    contact_person = nodeprop.String(name=_("Contact Person"), nullable=True)
    street_address = nodeprop.String(name=_("Street Address"), nullable=True)
    city = nodeprop.String(name=_("City"), nullable=True)
    region = nodeprop.String(name=_("Region"), nullable=True)
    postal_code = nodeprop.String(name=_("Postal Code"), nullable=True)
    country_code = nodeprop.String(name=_("Country"), nullable=True)
    website = nodeprop.String(name=_("Website"), nullable=True)
    email = nodeprop.String(name=_("Email"), nullable=True)
    telephone = nodeprop.String(name=_("Telephone"), nullable=True)
    fax = nodeprop.String(name=_("Fax"), nullable=True)
    contact_type = nodeprop.String(name=_("Contact Type"), nullable=True)
    note = nodeprop.String(name=_("Notes"), nullable=True)
    
    repository = djbulbs.models.SingleRelationField(AddressOf)
    objects = GraphManager()

    def __unicode__(self):
        return u"<%s: %s>" % (self.__class__.__name__, self.contact_person)


    def format(self):
        elems = [e.strip() for e in [
            self.street_address,
            self.postal_code,
            self.city,
            self.region,
            utils.country_name_from_code(self.country_code) \
                    if self.country_code else None
        ] if e is not None]
        return u"\n".join(elems).replace(", ", "\n")
djbulbs.graph.add_proxy(Contact.element_type, Contact)


class Authority(ResourceBase):
    """Model representing an archival authority."""
    element_type = "authority"

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    
    dates_of_existence = nodeprop.String(name=_("Dates of Existence"), nullable=True)
    functions = nodeprop.String(name=_("Functions"), nullable=True)
    general_context = nodeprop.String(name=_("General Context"), nullable=True)
    history = nodeprop.String(name=_("History"), nullable=True)
    institution_responsible_identifier = nodeprop.String(name=_("Institution Responsible Identifier"), nullable=True)
    internal_structures = nodeprop.String(name=_("Internal Structures"), nullable=True)
    legal_status = nodeprop.String(name=_("Legal Status"), nullable=True)
    mandates = nodeprop.String(name=_("Mandates"), nullable=True)
    places = nodeprop.String(name=_("Places"), nullable=True)
    revision_history = nodeprop.String(name=_("Revision History"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    @property
    def type_name(self):
        return terms.AUTHORITY_TYPES[self.type_of_entity][1]

    @cachedproperty
    def collection_set(self):
        return Collection.objects.filter(creator=self)

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Authority.element_type, Authority)


class Keyword(djbulbs.models.Model):
    """Model representing a keyword."""
    element_type = "keyword"
    name = nodeprop.String(name=_("Name"), nullable=False)

    objects = GraphManager()

    def _describes(self, model):
        return model.objects.outgoing(Describes, self)

    @cachedproperty
    def collection_set(self):
        return self._describes(Collection)

    @cachedproperty
    def repository_set(self):
        return self._describes(Repository)

    @cachedproperty
    def authority_set(self):
        return self._describes(Authority)

    def __unicode__(self):
        return self.name
djbulbs.graph.add_proxy(Keyword.element_type, Keyword)


class FuzzyDate(djbulbs.models.Model):
    """Model representing an approximate historical
    date or a date range."""
    element_type = "fuzzydate"
    CHOICES = (
            ("year", "Year"),
            ("month", "Month"),
            ("day", "Day"),
    )
    objects = GraphManager()
    collection = djbulbs.models.SingleRelationField(LocatesInTime)
    start_date = nodeprop.DateTime(name=_("Start Date"), indexed=True, nullable=False)
    end_date = nodeprop.DateTime(name=_("End Date"), indexed=True, nullable=True)
    precision = nodeprop.String(name=_("Precision"), nullable=True)
    circa = nodeprop.Integer(name=_("Circa"), nullable=True, default=0)

    @classmethod
    def from_fuzzy_date(cls, datestr):
        """Parse dates like "1939-1946", "c 1945" etc. This exists solely
        for importing dates from Aim25 web scrapes, and will go away some
        point in the future."""
        m1 = re.search("^(?P<start>\d{4})\s*-\s*(?P<end>\d{4})(?P<ish>s)?$", datestr.strip())
        fdate = FuzzyDate()
        if m1:
            d1 = datetime.datetime(int(m1.group("start")), 1, 1)
            d2 = datetime.datetime(int(m1.group("end")), 12, 31)
            fdate.start_date = d1
            fdate.end_date = d2
            fdate.circa = m1.group("ish") is not None
            fdate.precision = "year"
            return fdate
        m2 = re.search("^(?P<circa>c)?\s?(?P<year>\d{4})$", datestr.strip())
        if m2:
            d1 = datetime.datetime(int(m2.group("year")), 1, 1)
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
djbulbs.graph.add_proxy(FuzzyDate.element_type, FuzzyDate)

