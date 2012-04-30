"""
Import USHMM's 
"""

import os
import re
import sys
import json
from lxml import etree

import babel

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from portal import models

def gs(doc, attr):
    try: return doc.xpath(".//field[@name='" + attr + "']")[0].text
    except IndexError: pass

def gm(doc, attr):
    return [n.text for n in doc.xpath(".//field[@name='" + attr + "']")]

def stripdot(text):
    if text[-1] == ".":
        return text[:-1]
    return text

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """Run scrape."""
        # input a file containing urls to scrap
        if not len(args) == 1:
            raise CommandError("No input url file given.")

        # get a reverse dict of language-name -> code
        self.langcodes = dict([(v, k) for k, v in \
                babel.Locale("en").languages.iteritems()])

        # lookup the repository
        self.repo = models.Repository.objects.filter(othername__name="USHMM")[0]
        count = 0
        with transaction.commit_on_success():
            sys.stderr.write("Clearing current collections...\n")
            self.repo.collection_set.all().delete()
            with file(args[0], "r") as infile:
                for _, element in etree.iterparse(infile, tag="doc", strip_cdata=False):
                    for rectype in element.xpath(".//field[text()='Archives Collection ISAD(G)']"):
                        count += 1
                        sys.stderr.write("Extracting %d: %s\n" % (count, 
                                element.xpath(".//field[@name='irn']")[0].text))
                        self.import_item(element)

    def get_data(self, doc):
        """Extract XML doc node to a dictionary."""
        data = {}
        data["identifier"] = gs(doc, "irn")
        data["name"] = gs(doc, "collection_name") \
                or gs(doc, "title") \
                or gs(doc, "unit_title")
        data["acquisition"] = gs(doc, "acq_source")
        data["extent_and_medium"] = "\n".join(gm(doc, "extent"))
        data["scope_and_content"] = "\n".join(gm(doc, "scope_content"))
        data["arrangement"] = "\n".join(gm(doc, "arrangement"))
        data["languages"] = [self.langcodes.get(lang) for lang in gm(doc, "language")]
        data["sources"] = "\n".join(gm(doc, "provenance"))
        data["rules"] = "ISAD(G)"
        data["physical_characteristics"] = gs(doc, "dimensions")
        if gs(doc, "material_composition") is not None:
            if data["physical_characteristics"]:
                data["physical_characteristics"] += "\n"
            else:
                data["physical_characteristics"] = ""
            data["physical_characteristics"] += gs(doc, "material_composition")
        return data

    def get_dates(self, doc):
        """Extract related dates."""
        return gm(doc, "display_date")

    def get_creator(self, doc):
        return gs(doc, "creator_name_sort")

    def get_name_access(self, doc):
        """Get related name access points."""
        return self._get_subject_type(doc, "Personal Name")

    def _get_subject_type(self, doc, type):
        """Get subjects for a specific type of heading."""
        sh = gm(doc, "subject_heading")
        st = gm(doc, "subject_type")
        return [s for s, t in zip(sh, st) if t == type]

    def get_corporate_bodies(self, doc):
        """Get related corporate bodies."""
        return self._get_subject_type(doc, "Corporate Name")

    def get_subject_access(self, doc):
        """Get related corporate bodies."""
        return self._get_subject_type(doc, "Topical Term")
        
    def import_item(self, doc):
        """Import scraped data."""
        data = self.get_data(doc)
        if not data.get("name"):
            # can't do much with this then...
            return

        people = self.get_name_access(doc)
        corporations = self.get_corporate_bodies(doc)
        creator = self.get_creator(doc)
        subjects = self.get_subject_access(doc)
        dates = self.get_dates(doc)

        coll, _ = models.Collection.objects.get_or_create(
                repository=self.repo,
                **data
        )
        for sstr in subjects:
            coll.tags.add(*[stripdot(s) for s in sstr.split(" -- ")])

        for datestr in dates:
            fd = models.FuzzyDate.from_fuzzy_date(datestr)
            if fd:
                coll.date_set.add(fd)
        if creator:
            person = self.add_person(creator)
            if person:
                coll.creator = person
                coll.save()

        for pstring in people:
            person = self.add_person(pstring)
            if person:
                access = models.NameAccess(subject=person, object=coll)
                access.save()
                sys.stderr.write("Added person: %s\n" % person)

        for cstring in corporations:
            corp = self.add_corporation(cstring)
            if corp:
                access = models.NameAccess(subject=corp, object=coll)
                access.save()
                sys.stderr.write("Added corporate body: %s\n" % corp)


    def add_person(self, namestr):
        """Attempt to add person name."""
        if "family" in namestr.lower():
            return self.add_family(namestr)
        parts = [stripdot(p) for p in namestr.split(" -- ")]
        person, created = models.Person.objects.get_or_create(name=parts[0])
        if created:
            person.identifier = "person%06d" % models.Person.objects.count()
        for part in parts[1:]:
            if part[0] == "(" and part[-1] == ")":
                person.othername_set.add(models.OtherName(type=models.OtherName.OTHER,
                        name=part[1:-1]))
            elif re.search("\d{4}", part):
                person.dates_of_existence = part
        person.save()
        return person

    def add_family(self, namestr):
        """Add a family."""
        parts = [stripdot(p) for p in namestr.split(" -- ")]
        family, created = models.Family.objects.get_or_create(name=parts[0])
        if created:
            family.identifier = "family%06d" % models.Family.objects.count()
        for part in parts[1:]:
            if part[0] == "(" and part[-1] == ")":
                family.othername_set.add(models.OtherName(type=models.OtherName.OTHER,
                        name=part[1:-1]))
            elif re.search("\d{4}", part):
                family.dates_of_existence = part
        family.save()
        return family

    def add_corporation(self, desc):
        """Attempt to add a corporate name."""
        # nasty hack to get USHMM names in the same format as wiener library
        # FIXME: Get rid of this
        name = desc.split(" -- ")[0]\
                .replace("(Concentration camp)", "concentration camp")
        corp, created = models.CorporateBody.objects.get_or_create(name=name)
        if created:
            corp.identifier = "corp%06d" % models.CorporateBody.objects.count()
            corp.save()




