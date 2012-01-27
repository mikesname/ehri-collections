"""
Repository model.
"""
import datetime

from django.db import models

from ehriportal.repositories import utils
from ehriportal.archival_resource.models import ArchivalResource

from incf.countryutils import data as countrydata


class Repository(ArchivalResource):
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
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Contact, self).save()



