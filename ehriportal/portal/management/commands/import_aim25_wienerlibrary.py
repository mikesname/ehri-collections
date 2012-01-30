"""
Attempt to scape AIM25's Wiener Library material.
"""

import os
import re
import sys
import json
import httplib2
import urllib

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from ehriportal.portal import models

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

BASEURL = "http://www.aim25.ac.uk"
INSTID = 104
PAGES = 56 # 56


def get_page_soup(url):
    """Get a BeautifulSoup object for a given page."""
    http = httplib2.Http()
    resp, content = http.request(url)
    return BeautifulSoup(content)


def search_aim25(instid=INSTID, page=1):
    """Run a post query."""
    # 1. run an advanced search.  Scape the page
    # 2. for the number of result pages
    # 3. for each page, scape the links
    url = "/cgi-bin/vcdf/asearch?"
    params = dict(
            inst_id=instid,
            pageno=page
    )
    query = urllib.urlencode(params)
    soup = get_page_soup(BASEURL + url + query)
    links = []
    for tr in soup.find("div", id="content").find("table").findAll("tr")[1:]:
        links.append(BASEURL + tr.find("a").attrs[0][1])
    return links


def get_identity_details(soup):
    """Scape the identity section."""
    idfields = dict(
            identifier="Reference code(s)",
            name="Full title",
            dates="Date(s)",
            lod="Level of description",
            extent_and_medium="Extent",
            name_of_creators="Name of creator(s)"
    )
    ids = dict()
    table = soup.find("div", id="content").find("table")
    for tr in table.findAll("tr"):
        for key, val in idfields.iteritems():
            if tr.find(text=val):
                ids[key] = re.sub("^:\s+", "", tr.findAll("td")[1].text)
                break
    return ids

def get_paragraph_divided(soup):
    """Scape sections consisting of paragraph header/content."""
    sections = dict(
            archival_history="Administrative/Biographical history",
            scope_and_content="Scope and content/abstract",
            arrangement="System of arrangement",
            access_conditions="Conditions governing access",
            reproduction_conditions="Conditions governing reproduction",
            finding_aids="Finding aids",
            sources="Immediate source of acquisition"
    )
    sects = dict()
    for key, val in sections.iteritems():
        text = u""
        p = soup.find("h2", text=val).parent.parent
        for pn in p.nextSiblingGenerator():
            if hasattr(pn, "name"):
                if pn.name == "h2" or pn.find("strong"):
                    break
                if pn.name == 'p':
                    text += "%s\n\n" % pn.text.strip()
        sects[key] = text.strip()
    return sects


def get_break_divided(soup):
    """Scrape sections divided by break: header/content."""
    sections = dict(
            language="Language/scripts of material",
            archivist_note="Archivist's note",
            rules_conventsion="Rules or conventions",
            dates_of_description="Date(s) of descriptions",
            related_materials="Related material",
            publication_note="Publication note"            
    )
    sects = dict()
    for key, val in sections.iteritems():
        p = soup.find("h2", text=val).parent.parent
        parts = [c for c in p.childGenerator()]
        if len(parts) == 4:
            sects[key] = re.sub("^:\s+", "", parts[3].strip())
        else:
            sects[key] = u''
    return sects


def get_keywords(soup):
    """Get keywords, represented as checkboxes."""
    head = soup.find("h2", text="Related Subject Search")
    if head is None:
        return []
    div = head.parent.parent.parent
    attrs = [i.attrMap["value"] for i in \
            div.findAll("input", {"name": "keyword"})]
    return [urllib.unquote(a) for a in attrs]


def get_person_names(soup):
    """Get person names, represented as checkboxes."""
    head = soup.find("h2", text="Related Personal Name Search")
    if head is None:
        return []
    div = head.parent.parent.parent
    attrs = [i.attrMap["value"] for i in \
            div.findAll("input", {"name": "keyword"})]
    return [urllib.unquote(a) for a in attrs]


def scrape_item(url):
    """Scrape a collection's details."""
    # this will be fugly
    soup = get_page_soup(url)
    ids = get_identity_details(soup)
    brs = get_break_divided(soup)
    prs = get_paragraph_divided(soup)
    keywords = get_keywords(soup)
    persons = get_person_names(soup)
    info = dict(ids.items() + brs.items() + prs.items())
    info["keywords"] = keywords
    info["people"] = persons
    return info


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """Run scrape."""
        # input a file containing urls to scrap
        if not len(args) == 1:
            raise CommandError("No input url file given.")
        
        self.wiener = models.Repository.objects.filter(name="Wiener Library")[0]
        sys.stderr.write("Clearing current collections...\n")
        self.wiener.collection_set.all().delete()
        with open(args[0], "r") as infile:
            with transaction.commit_on_success():
                for line in infile.readlines():
                    url = line.strip()
                    if not url:
                        continue
                    sys.stderr.write("Scraping url: %s\n" % url)
                    item = scrape_item(url)
                    self.import_item(item)

    def import_item(self, data):
        """Import scraped data."""

        coll, _ = models.Collection.objects.get_or_create(
                repository=self.wiener,
                identifier=data.get("identifier"),
                name=data.get("name"),
                access_conditions=data.get("access_conditions"),
                accruals=data.get("accruals"),
                acquisition=data.get("acquisition"),
                appraisal=data.get("appraisal"),
                archival_history=data.get("archival_history"),
                arrangement=data.get("arrangement"),
                edition=data.get("edition"),
                extent_and_medium=data.get("extent_and_medium"),
                finding_aids=data.get("finding_aids"),
                institution_responsible_identifier=data.get("institution_responsible_identifier"),
                location_of_copies=data.get("location_of_copies"),
                location_of_originals=data.get("location_of_originals"),
                physical_characteristics=data.get("physical_characteristics"),
                related_units_of_description=data.get("related_units_of_description"),
                reproduction_conditions=data.get("reproduction_conditions"),
                revision_history=data.get("revision_history"),
                rules=data.get("rules"),
                scope_and_content=data.get("scope_and_content"),
                sources=data.get("sources")
        )
        coll.save()
        coll.tags.add(*data["keywords"])
        fd = models.FuzzyDate.from_fuzzy_date(data["dates"])
        if fd:
            coll.dates.add(fd)

