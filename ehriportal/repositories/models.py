"""
Repository model.
"""
import datetime

from django.db import models

class Repository(models.Model):
    """Repository."""
    ENTITY_TYPES=()
    LOD = ()

    identifier = models.CharField(max_length=255)
    authorized_form_of_name = models.CharField(max_length=255)
    lod = models.CharField(max_length=255, choices=LOD)
    type_of_entity = models.CharField(max_length=255, choices=ENTITY_TYPES)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)
    # optional translatable text fields
    access_conditions = models.TextField(null=True, blank=True)
    buildings = models.TextField(null=True, blank=True)
    collecting_policies = models.TextField(null=True, blank=True)
    dates_of_existence = models.TextField(null=True, blank=True)
    disabled_access = models.TextField(null=True, blank=True)
    finding_aids = models.TextField(null=True, blank=True)
    functions = models.TextField(null=True, blank=True)
    general_context = models.TextField(null=True, blank=True)
    geocultural_context = models.TextField(null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    holdings = models.TextField(null=True, blank=True)
    internal_structures = models.TextField(null=True, blank=True)
    legal_status = models.TextField(null=True, blank=True)
    maintenance_notes = models.TextField(null=True, blank=True)
    mandates = models.TextField(null=True, blank=True)
    opening_times = models.TextField(null=True, blank=True)
    places = models.TextField(null=True, blank=True)
    reproduction_services = models.TextField(null=True, blank=True)
    research_services = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    sources = models.TextField(null=True, blank=True)

    def save(self):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Repository, self).save()

    def __unicode__(self):
        return self.identifier


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
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Contact, self).save()


class OtherName(models.Model):
    name = models.CharField(max_length=255)
    repository = models.ForeignKey(Repository, related_name="other_names")



