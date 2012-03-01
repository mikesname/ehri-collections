"""Geocode Contact objects."""

import sys

from geopy import geocoders

from django.core.management.base import BaseCommand, CommandError

from portal import models


class Command(BaseCommand):
    """Set lat/long fields on contacts with a street address,
    currently just using Google's geocoder."""
    def handle(self, *args, **kwargs):
        """Run geocode."""
        self.geocoder = geocoders.GeoNames()

        for contact in models.Contact.objects.all():
            self.geocode_contact(contact)

    def geocode_contact(self, contact):
        """Set lat/long fields on contact objects."""
        if contact.street_address:
            sys.stderr.write("Geocoding: %s: %s\n" % (contact.repository.name, contact.format()))
            try:
                formaddr, latlon = self.geocoder.geocode(contact.format().encode("utf8"))
            except ValueError:
                sys.stderr.write(" - More than one value found!\n")
            except geocoders.google.GTooManyQueriesError:
                raise CommandError("Too many queries for Google Geocode.")
            except geocoders.google.GQueryError:
                sys.stderr.write(" - Unable to get latlong for address\n")
            else:
                contact.lat = latlon[0]
                contact.lon = latlon[1]
                contact.save()
                sys.stderr("Set lat/lon: %s, %s\n\n" % latlon)


        

