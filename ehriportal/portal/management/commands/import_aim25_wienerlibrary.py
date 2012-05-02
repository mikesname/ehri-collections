"""
Attempt to scape AIM25's Wiener Library material.
"""

import os
import re
import sys
import json
import datetime

from django.db import transaction
from django.db.models import signals
from django.core import management
from django.core.management.base import BaseCommand, CommandError

from portal import models



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """Run scrape."""
        # input a file containing urls to scrap
        if not len(args) == 1:
            raise CommandError("No input json file given.")

        # disconnect Haystack realtime signals
        signals.pre_save.disconnect(dispatch_uid="setup_index_signals")
        signals.pre_delete.disconnect(dispatch_uid="setup_index_signals")

        starttime = datetime.datetime.now()

        # lookup the repository
        self.repo = models.Repository.objects.filter(name="Wiener Library")[0]
        with open(args[0], "r") as infile:
            inputs = json.load(infile)
            with transaction.commit_on_success():
                for item in inputs:
                    sys.stderr.write("Importing %s\n" % item.get("name"))
                    self.import_item(item)

        # update the haystack index for Collections
        management.call_command("update_index", "portal.Collection", "portal.Authority",
                interactive=False, start_date=starttime.isoformat(), remove=True)

    def import_item(self, data):
        """Import scraped data."""

        created = False
        identifier = data.pop("identifier")
        try:
            coll = models.Collection.objects.get(
                    repository=self.repo, identifier=identifier)
        except models.Collection.DoesNotExist:
            coll = models.Collection(
                    repository=self.repo, identifier=identifier)
            created = True

        keywords = data.pop("keywords")
        people = data.pop("people")
        corps = data.pop("corps")
        dates = data.pop("dates")
        creator = data.pop("name_of_creators")

        for attr, val in data.items():
            setattr(coll, attr, val)
        
        if creator:
            person = self.add_person(creator)
            if person:
                coll.creator = person

        coll.save()
        coll.tags.add(*keywords)
        fd = models.FuzzyDate.from_fuzzy_date(dates)
        if fd:
            coll.date_set.add(fd)


        for pstring in people:
            person = self.add_person(pstring)
            if person:
                access = models.NameAccess(subject=person, object=coll)
                access.save()
                sys.stderr.write("Added person: %s\n" % person)

        for cstring in corps:
            corp = self.add_corporation(cstring)
            if corp:
                access = models.NameAccess(subject=corp, object=coll)
                access.save()
                sys.stderr.write("Added corporate body: %s\n" % corp)

    def add_person(self, desc):
        """Attempt to add person name from Aim25s dodgy string."""
        if "family" in desc.lower():
            return self.add_family(desc)

        # typical string looks like
        # LastName | FirstName | Othername | b 1939 | Occupation | stuff 
        # ... so we need to find the first cell that looks like a date,
        # put everything before it in a name, everything after in history
        plist = [s.strip() for s in desc.split("|")]
        dateidx = None
        for i, s in enumerate(plist):
            if re.search("\d{4}", s):
                dateidx = i
                break
        if dateidx is None and len(plist) < 2:
            return
        name = None
        kwargs = {}
        if dateidx is None:
            name = "%s, %s" % (plist[0], " ".join(plist[1:]))
        else:
            names = plist[:dateidx]
            if not names:
                sys.stderr.write("BAD NAME STRING: %s\n" % desc)
                return
            name = "%s, %s" % (names[0], " ".join(names[1:]))
            kwargs["dates_of_existence"] = plist[dateidx]
            kwargs["history"] = "\n".join(plist[dateidx+1:])
        person, created = models.Person.objects.get_or_create(name=name, defaults=kwargs)
        if created:
            person.identifier = "person%06d" % models.Person.objects.count()
        person.save()
        return person


    def add_family(self, desc):
        """Add a family."""
        plist = [s.strip() for s in desc.split("|")]
        try:
            family, created = models.Family.objects.get_or_create(name=plist[0])
            if created:
                family.identifier = "family%06d" % models.Family.objects.count()
            family.save()
            return family
        except IndexError:
            pass

    def add_corporation(self, desc):
        """Attempt to add a corporate name."""
        plist = [s.strip() for s in desc.split("|")]
        try:
            names = plist[0].split(" x ")
            corp, created = models.CorporateBody.objects.get_or_create(name=names[0])
            if created:
                corp.identifier = "corp%06d" % models.CorporateBody.objects.count()
            corp.save()
            for name in names[1:]:
                on, created = models.OtherFormOfName.objects.get_or_create(name=name, resource=corp)
                if created: on.save()
            return corp
        except IndexError:
            pass



