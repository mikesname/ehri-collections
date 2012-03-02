"""Geocode Contact objects."""

import sys
import time

from geopy import geocoders

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from portal import models


class Command(BaseCommand):
    """Set lat/long fields on contacts with a street address,
    currently just using Google's geocoder."""
    def handle(self, *args, **kwargs):
        """Run geocode."""
        appid = getattr(settings, "YAHOO_APP_ID", None)
        if appid is not None:
            self.geocoder = geocoders.Yahoo(appid)
        else:
            self.geocoder = geocoders.Google()


        for contact in models.Contact.objects.all():
            self.geocode_contact(contact)

    def geocode_contact(self, contact):
        """Set lat/long fields on contact objects."""
        if contact.street_address and not contact.latitude:
            sys.stderr.write("Geocoding: %s: %s\n" % (contact.repository.name, contact.format()))
            try:
                formaddr, (lat, lon) = self.geocoder.geocode(contact.format().encode("utf8"))
            except ValueError:
                sys.stderr.write(" - More than one value found!\n")
            except geocoders.google.GTooManyQueriesError:
                raise CommandError("Too many queries for Google Geocode.")
            except geocoders.google.GQueryError:
                sys.stderr.write(" - Unable to get latlong for address\n")
            else:
                contact.latitude = lat
                contact.longitude = lon
                contact.save()
                sys.stderr.write("Set lat/lon: %s, %s\n\n" % (lat, lon))
                # delay to keep Google rate limit happy (hopefully)
                time.sleep(0.25)


        

