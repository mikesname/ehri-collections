"""Geocode Contact objects."""

import sys
import time
from optparse import make_option

from geopy import geocoders

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.gis import geos

from portal import models


class Command(BaseCommand):
    """Set lat/long fields on contacts with a street address,
    currently just using Google's geocoder."""
    option_list = BaseCommand.option_list + (
        make_option('--geocoder',
            dest='geocoder',
            default="yahoo",
            choices=["yahoo", "google"],
            help='Geocoder to use'),
        )

    def handle(self, *args, **options):
        """Run geocode."""
        appid = getattr(settings, "YAHOO_APP_ID", None)
        if not "google" in options["geocoder"] and appid is not None:
            self.geocoder = geocoders.Yahoo(appid)
            sys.stderr.write("Geocoding with Yahoo world...\n")
        else:
            self.geocoder = geocoders.Google()
            sys.stderr.write("Geocoding with Google maps...\n")


        for repo in models.Repository.objects.all():
            self.geocode_contact(repo)

    def geocode_contact(self, resource):
        """Set lat/long fields on contact objects."""
        contact = resource.primary_contact
        if resource.place_set.count() == 0 and contact and contact.street_address:
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
                point = models.Place(point=geos.Point(lat, lon), 
                        resource=resource)
                point.save()
                sys.stderr.write("Set lat/lon: %s, %s\n\n" % (lat, lon))
                # delay to keep Google rate limit happy (hopefully)
                time.sleep(0.05)


        

