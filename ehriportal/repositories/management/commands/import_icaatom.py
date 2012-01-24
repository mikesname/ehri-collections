"""
Post Repos to a Solr engine.
"""

from optparse import make_option
import unicodedata
import urllib
import httplib2
import json

from django.core.management.base import BaseCommand, CommandError
from ehriportal.repositories.models import Repository as DjRepository

from incf.countryutils import data as countrydata
from sqlaqubit import models, keys, create_engine, init_models
from sqlalchemy.engine.url import URL
from sqlalchemy import and_


class ImportICAAtomCommand(BaseCommand):
    """Import repositories from ICA Atom."""
    option_list - BaseCommand.option_list + (
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
            username=self.options.dbuser,
            password=self.options.dbpass,
            host=self.options.dbhost,
            database=self.options.database,
            port=self.options.dbport,
            query=dict(
                charset="utf8", 
                use_unicode=0
            )
        ))
        init_models(engine)
        self.session = models.Session()
        
        repos = self.session.query(models.Repository).all()

        for repo in repos:
            if not repo.identifier:
                self.stderr.write("\n\nCannot index repository with no identifier\n")
                continue
            self.stderr.write("\n\nIndexing repo: %s\n" % repo.identifier)
            self.import_icaatom_repo(repo)


    def import_icaatom_repo(repo):
        """Import individual repository."""

        i18n = repo.get_i18n()

        djrepo = DjRepository(
            identifier=repo.identifier,
            # TODO
        )


