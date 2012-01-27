"""
Post Repos to a Solr engine.
"""

from optparse import make_option
import unicodedata
import urllib
import httplib2
import json

from django.core.management.base import BaseCommand, CommandError
from ehriportal.repositories.models import Repository as DjRepository, \
        Contact as DjContact
from ehriportal.archival_resource.models import OtherName
from ehriportal.descriptions.models import Description

from incf.countryutils import data as countrydata
import phpserialize
from sqlaqubit import models, keys, create_engine, init_models
from sqlalchemy.engine.url import URL
from sqlalchemy import and_


class Command(BaseCommand):
    """Import repositories from ICA Atom."""
    option_list = BaseCommand.option_list + (
        make_option(
                "-U",
                "--dbuser",
                action="store",
                dest="dbuser",
                default="qubit",
                help="Database user"),
        make_option(
                "-p",
                "--dbpass",
                action="store",
                dest="dbpass",
                help="Database password"),
        make_option(
                "-H",
                "--dbhost",
                action="store",
                dest="dbhost",
                default="localhost",
                help="Database host name"),
        make_option(
                "-P",
                "--dbport",
                action="store",
                dest="dbport",
                help="Database port"),
        make_option(
                "-D",
                "--database",
                action="store",
                dest="database",
                default="qubit",
                help="Database name"),
    )
    
    def handle(self, *args, **options):
        """Perform import."""

        engine = create_engine(URL("mysql",
            username=options["dbuser"],
            password=options["dbpass"],
            host=options["dbhost"],
            database=options["database"],
            port=options["dbport"],
            query=dict(
                charset="utf8", 
                use_unicode=0
            )
        ))
        init_models(engine)
        self.session = models.Session()

        # random selection for now
        repos = []
        repos.extend(self.session.query(models.Repository)\
                .filter(models.Repository.identifier=='ehri1691None').all())
        repos.extend(self.session.query(models.Repository).all()[50:150])
        self.stdout.write("Adding %s repos\n" % len(repos))
        for repo in repos:
            if not repo.identifier:
                self.stderr.write("\n\nCannot index repository with no identifier\n")
                continue
            self.stderr.write("\n\nIndexing repo: %s\n" % repo.identifier)
            self.import_icaatom_repo(repo)


    def import_icaatom_repo(self, repo):
        """Import individual repository."""

        i18n = repo.get_i18n()

        djrepo = DjRepository(
            identifier=repo.identifier,
            # TODO contacts, maintanence notes
            name=i18n["authorized_form_of_name"],
            access_conditions=i18n["access_conditions"],
            buildings=i18n["buildings"],
            collecting_policies=i18n["collecting_policies"],
            dates_of_existence=i18n["dates_of_existence"],
            disabled_access=i18n["disabled_access"],
            finding_aids=i18n["finding_aids"],
            functions=i18n["functions"],
            general_context=i18n["general_context"],
            geocultural_context=i18n["geocultural_context"],
            history=i18n["history"],
            holdings=i18n["holdings"],
            internal_structures=i18n["internal_structures"],
            legal_status=i18n["legal_status"],
            mandates=i18n["mandates"],
            opening_times=i18n["opening_times"],
            places=i18n["places"],
            reproduction_services=i18n["reproduction_services"],
            research_services=i18n["research_services"],
            rules=i18n["rules"],
            sources=i18n["sources"],
        )
        djrepo.save()
        for contact in repo.contacts:
            self.import_icaatom_contact(djrepo, contact)
        for on in repo.other_names:            
            djrepo.othername_set.add(OtherName(name=on.get_i18n()["name"],
                    resource=djrepo))
        for io in repo.information_objects:
            self.import_icaatom_description(djrepo, io)


    def import_icaatom_contact(self, djrepo, contact):
        """Import a contact detail object."""

        i18n = contact.get_i18n()

        djcontact = DjContact(
            repository=djrepo,
            primary=contact.primary_contact,
            contact_person=contact.contact_person,
            country_code=contact.country_code,
            postal_code=contact.postal_code,
            street_address=contact.street_address,
            telephone=contact.telephone,
            fax=contact.fax,
            email=contact.email,
            website=contact.website,
            longitude=contact.longitude,
            latitude=contact.latitude,
            city=i18n["city"],
            region=i18n["region"],
            note=i18n["note"]
        )
        djcontact.save()

    def import_icaatom_description(self, djrepo, desc):
        """Import an archival description/information object."""
        i18n = desc.get_i18n()
        djdesc = Description(
                repository=djrepo,
                identifier=desc.identifier,
                name=i18n["title"],
                access_conditions=i18n["access_conditions"],
                accruals=i18n["accruals"],
                acquisition=i18n["acquisition"],
                alternate_title=i18n["alternate_title"],
                appraisal=i18n["appraisal"],
                archival_history=i18n["archival_history"],
                arrangement=i18n["arrangement"],
                edition=i18n["edition"],
                extent_and_medium=i18n["extent_and_medium"],
                finding_aids=i18n["finding_aids"],
                institution_responsible_identifier=i18n["institution_responsible_identifier"],
                location_of_copies=i18n["location_of_copies"],
                location_of_originals=i18n["location_of_originals"],
                physical_characteristics=i18n["physical_characteristics"],
                related_units_of_description=i18n["related_units_of_description"],
                reproduction_conditions=i18n["reproduction_conditions"],
                revision_history=i18n["revision_history"],
                rules=i18n["rules"],
                scope_and_content=i18n["scope_and_content"],
                sources=i18n["sources"]
        )
        # FIXME: Description could have many languages
        djdesc.save()
        for prop in desc.properties:
            if prop.name == "language" or prop.name == "languageOfDescription":
                vals = phpserialize.loads(prop.get_i18n()["value"])
                for index, val in vals.iteritems():
                    djdesc.set_property(prop.name, val)


