# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Contact.contact_type_en'
        db.add_column('portal_contact', 'contact_type_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.city_en'
        db.add_column('portal_contact', 'city_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.region_en'
        db.add_column('portal_contact', 'region_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.note_en'
        db.add_column('portal_contact', 'note_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_en'
        db.add_column('portal_repository', 'access_conditions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_en'
        db.add_column('portal_repository', 'buildings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_en'
        db.add_column('portal_repository', 'collecting_policies_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_en'
        db.add_column('portal_repository', 'dates_of_existence_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_en'
        db.add_column('portal_repository', 'disabled_access_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_en'
        db.add_column('portal_repository', 'finding_aids_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.functions_en'
        db.add_column('portal_repository', 'functions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.general_context_en'
        db.add_column('portal_repository', 'general_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_en'
        db.add_column('portal_repository', 'geocultural_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.history_en'
        db.add_column('portal_repository', 'history_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.holdings_en'
        db.add_column('portal_repository', 'holdings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.internal_structures_en'
        db.add_column('portal_repository', 'internal_structures_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.legal_status_en'
        db.add_column('portal_repository', 'legal_status_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.maintenance_notes_en'
        db.add_column('portal_repository', 'maintenance_notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.mandates_en'
        db.add_column('portal_repository', 'mandates_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_en'
        db.add_column('portal_repository', 'opening_times_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.places_en'
        db.add_column('portal_repository', 'places_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_en'
        db.add_column('portal_repository', 'reproduction_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_en'
        db.add_column('portal_repository', 'research_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_en'
        db.add_column('portal_repository', 'rules_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.sources_en'
        db.add_column('portal_repository', 'sources_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Contact.contact_type_en'
        db.delete_column('portal_contact', 'contact_type_en')

        # Deleting field 'Contact.city_en'
        db.delete_column('portal_contact', 'city_en')

        # Deleting field 'Contact.region_en'
        db.delete_column('portal_contact', 'region_en')

        # Deleting field 'Contact.note_en'
        db.delete_column('portal_contact', 'note_en')

        # Deleting field 'Repository.access_conditions_en'
        db.delete_column('portal_repository', 'access_conditions_en')

        # Deleting field 'Repository.buildings_en'
        db.delete_column('portal_repository', 'buildings_en')

        # Deleting field 'Repository.collecting_policies_en'
        db.delete_column('portal_repository', 'collecting_policies_en')

        # Deleting field 'Repository.dates_of_existence_en'
        db.delete_column('portal_repository', 'dates_of_existence_en')

        # Deleting field 'Repository.disabled_access_en'
        db.delete_column('portal_repository', 'disabled_access_en')

        # Deleting field 'Repository.finding_aids_en'
        db.delete_column('portal_repository', 'finding_aids_en')

        # Deleting field 'Repository.functions_en'
        db.delete_column('portal_repository', 'functions_en')

        # Deleting field 'Repository.general_context_en'
        db.delete_column('portal_repository', 'general_context_en')

        # Deleting field 'Repository.geocultural_context_en'
        db.delete_column('portal_repository', 'geocultural_context_en')

        # Deleting field 'Repository.history_en'
        db.delete_column('portal_repository', 'history_en')

        # Deleting field 'Repository.holdings_en'
        db.delete_column('portal_repository', 'holdings_en')

        # Deleting field 'Repository.internal_structures_en'
        db.delete_column('portal_repository', 'internal_structures_en')

        # Deleting field 'Repository.legal_status_en'
        db.delete_column('portal_repository', 'legal_status_en')

        # Deleting field 'Repository.maintenance_notes_en'
        db.delete_column('portal_repository', 'maintenance_notes_en')

        # Deleting field 'Repository.mandates_en'
        db.delete_column('portal_repository', 'mandates_en')

        # Deleting field 'Repository.opening_times_en'
        db.delete_column('portal_repository', 'opening_times_en')

        # Deleting field 'Repository.places_en'
        db.delete_column('portal_repository', 'places_en')

        # Deleting field 'Repository.reproduction_services_en'
        db.delete_column('portal_repository', 'reproduction_services_en')

        # Deleting field 'Repository.research_services_en'
        db.delete_column('portal_repository', 'research_services_en')

        # Deleting field 'Repository.rules_en'
        db.delete_column('portal_repository', 'rules_en')

        # Deleting field 'Repository.sources_en'
        db.delete_column('portal_repository', 'sources_en')


    models = {
        'portal.collection': {
            'Meta': {'object_name': 'Collection', '_ormbases': ['portal.Resource']},
            'access_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'accruals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'acquisition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alternate_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'appraisal': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'archival_history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'arrangement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent_and_medium': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'institution_responsible_identifier': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_copies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_originals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'physical_characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_units_of_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portal.Repository']"}),
            'reproduction_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['portal.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'revision_history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'scope_and_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'portal.contact': {
            'Meta': {'object_name': 'Contact'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_type_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_type_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_type_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['portal.Repository']"}),
            'street_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'portal.othername': {
            'Meta': {'object_name': 'OtherName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portal.Resource']"})
        },
        'portal.property': {
            'Meta': {'object_name': 'Property'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portal.Resource']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'portal.repository': {
            'Meta': {'object_name': 'Repository', '_ormbases': ['portal.Resource']},
            'access_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dates_of_existence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dates_of_existence_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dates_of_existence_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dates_of_existence_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_access': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_access_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_access_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_access_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geocultural_context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geocultural_context_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geocultural_context_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geocultural_context_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holdings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holdings_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holdings_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holdings_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internal_structures': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_notes_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_notes_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opening_times': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opening_times_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opening_times_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opening_times_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['portal.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'portal.resource': {
            'Meta': {'object_name': 'Resource'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['portal']
