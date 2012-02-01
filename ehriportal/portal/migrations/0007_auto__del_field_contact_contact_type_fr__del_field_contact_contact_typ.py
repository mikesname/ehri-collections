# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Contact.contact_type_fr'
        db.delete_column('portal_contact', 'contact_type_fr')

        # Deleting field 'Contact.contact_type_de'
        db.delete_column('portal_contact', 'contact_type_de')

        # Deleting field 'Contact.note_fr'
        db.delete_column('portal_contact', 'note_fr')

        # Deleting field 'Contact.city_fr'
        db.delete_column('portal_contact', 'city_fr')

        # Deleting field 'Contact.contact_type_en'
        db.delete_column('portal_contact', 'contact_type_en')

        # Deleting field 'Contact.region_fr'
        db.delete_column('portal_contact', 'region_fr')

        # Deleting field 'Contact.note_de'
        db.delete_column('portal_contact', 'note_de')

        # Deleting field 'Contact.region_de'
        db.delete_column('portal_contact', 'region_de')

        # Deleting field 'Contact.note_en'
        db.delete_column('portal_contact', 'note_en')

        # Deleting field 'Contact.city_en'
        db.delete_column('portal_contact', 'city_en')

        # Deleting field 'Contact.region_en'
        db.delete_column('portal_contact', 'region_en')

        # Deleting field 'Contact.city_de'
        db.delete_column('portal_contact', 'city_de')

        # Deleting field 'Repository.rules_en'
        db.delete_column('portal_repository', 'rules_en')

        # Deleting field 'Repository.internal_structures_de'
        db.delete_column('portal_repository', 'internal_structures_de')

        # Deleting field 'Repository.finding_aids_de'
        db.delete_column('portal_repository', 'finding_aids_de')

        # Deleting field 'Repository.mandates_de'
        db.delete_column('portal_repository', 'mandates_de')

        # Deleting field 'Repository.functions_en'
        db.delete_column('portal_repository', 'functions_en')

        # Deleting field 'Repository.dates_of_existence_en'
        db.delete_column('portal_repository', 'dates_of_existence_en')

        # Deleting field 'Repository.places_de'
        db.delete_column('portal_repository', 'places_de')

        # Deleting field 'Repository.history_de'
        db.delete_column('portal_repository', 'history_de')

        # Deleting field 'Repository.collecting_policies_de'
        db.delete_column('portal_repository', 'collecting_policies_de')

        # Deleting field 'Repository.disabled_access_fr'
        db.delete_column('portal_repository', 'disabled_access_fr')

        # Deleting field 'Repository.internal_structures_en'
        db.delete_column('portal_repository', 'internal_structures_en')

        # Deleting field 'Repository.legal_status_de'
        db.delete_column('portal_repository', 'legal_status_de')

        # Deleting field 'Repository.rules_de'
        db.delete_column('portal_repository', 'rules_de')

        # Deleting field 'Repository.maintenance_notes_fr'
        db.delete_column('portal_repository', 'maintenance_notes_fr')

        # Deleting field 'Repository.functions_de'
        db.delete_column('portal_repository', 'functions_de')

        # Deleting field 'Repository.history_en'
        db.delete_column('portal_repository', 'history_en')

        # Deleting field 'Repository.holdings_fr'
        db.delete_column('portal_repository', 'holdings_fr')

        # Deleting field 'Repository.disabled_access_en'
        db.delete_column('portal_repository', 'disabled_access_en')

        # Deleting field 'Repository.places_en'
        db.delete_column('portal_repository', 'places_en')

        # Deleting field 'Repository.sources_de'
        db.delete_column('portal_repository', 'sources_de')

        # Deleting field 'Repository.maintenance_notes_en'
        db.delete_column('portal_repository', 'maintenance_notes_en')

        # Deleting field 'Repository.buildings_fr'
        db.delete_column('portal_repository', 'buildings_fr')

        # Deleting field 'Repository.general_context_de'
        db.delete_column('portal_repository', 'general_context_de')

        # Deleting field 'Repository.history_fr'
        db.delete_column('portal_repository', 'history_fr')

        # Deleting field 'Repository.legal_status_fr'
        db.delete_column('portal_repository', 'legal_status_fr')

        # Deleting field 'Repository.rules_fr'
        db.delete_column('portal_repository', 'rules_fr')

        # Deleting field 'Repository.opening_times_fr'
        db.delete_column('portal_repository', 'opening_times_fr')

        # Deleting field 'Repository.finding_aids_en'
        db.delete_column('portal_repository', 'finding_aids_en')

        # Deleting field 'Repository.maintenance_notes_de'
        db.delete_column('portal_repository', 'maintenance_notes_de')

        # Deleting field 'Repository.mandates_en'
        db.delete_column('portal_repository', 'mandates_en')

        # Deleting field 'Repository.dates_of_existence_de'
        db.delete_column('portal_repository', 'dates_of_existence_de')

        # Deleting field 'Repository.general_context_en'
        db.delete_column('portal_repository', 'general_context_en')

        # Deleting field 'Repository.collecting_policies_en'
        db.delete_column('portal_repository', 'collecting_policies_en')

        # Deleting field 'Repository.opening_times_en'
        db.delete_column('portal_repository', 'opening_times_en')

        # Deleting field 'Repository.holdings_en'
        db.delete_column('portal_repository', 'holdings_en')

        # Deleting field 'Repository.research_services_fr'
        db.delete_column('portal_repository', 'research_services_fr')

        # Deleting field 'Repository.geocultural_context_de'
        db.delete_column('portal_repository', 'geocultural_context_de')

        # Deleting field 'Repository.reproduction_services_en'
        db.delete_column('portal_repository', 'reproduction_services_en')

        # Deleting field 'Repository.general_context_fr'
        db.delete_column('portal_repository', 'general_context_fr')

        # Deleting field 'Repository.buildings_de'
        db.delete_column('portal_repository', 'buildings_de')

        # Deleting field 'Repository.opening_times_de'
        db.delete_column('portal_repository', 'opening_times_de')

        # Deleting field 'Repository.dates_of_existence_fr'
        db.delete_column('portal_repository', 'dates_of_existence_fr')

        # Deleting field 'Repository.access_conditions_fr'
        db.delete_column('portal_repository', 'access_conditions_fr')

        # Deleting field 'Repository.reproduction_services_de'
        db.delete_column('portal_repository', 'reproduction_services_de')

        # Deleting field 'Repository.internal_structures_fr'
        db.delete_column('portal_repository', 'internal_structures_fr')

        # Deleting field 'Repository.research_services_de'
        db.delete_column('portal_repository', 'research_services_de')

        # Deleting field 'Repository.legal_status_en'
        db.delete_column('portal_repository', 'legal_status_en')

        # Deleting field 'Repository.access_conditions_en'
        db.delete_column('portal_repository', 'access_conditions_en')

        # Deleting field 'Repository.finding_aids_fr'
        db.delete_column('portal_repository', 'finding_aids_fr')

        # Deleting field 'Repository.mandates_fr'
        db.delete_column('portal_repository', 'mandates_fr')

        # Deleting field 'Repository.geocultural_context_fr'
        db.delete_column('portal_repository', 'geocultural_context_fr')

        # Deleting field 'Repository.disabled_access_de'
        db.delete_column('portal_repository', 'disabled_access_de')

        # Deleting field 'Repository.sources_en'
        db.delete_column('portal_repository', 'sources_en')

        # Deleting field 'Repository.access_conditions_de'
        db.delete_column('portal_repository', 'access_conditions_de')

        # Deleting field 'Repository.reproduction_services_fr'
        db.delete_column('portal_repository', 'reproduction_services_fr')

        # Deleting field 'Repository.functions_fr'
        db.delete_column('portal_repository', 'functions_fr')

        # Deleting field 'Repository.research_services_en'
        db.delete_column('portal_repository', 'research_services_en')

        # Deleting field 'Repository.geocultural_context_en'
        db.delete_column('portal_repository', 'geocultural_context_en')

        # Deleting field 'Repository.collecting_policies_fr'
        db.delete_column('portal_repository', 'collecting_policies_fr')

        # Deleting field 'Repository.holdings_de'
        db.delete_column('portal_repository', 'holdings_de')

        # Deleting field 'Repository.sources_fr'
        db.delete_column('portal_repository', 'sources_fr')

        # Deleting field 'Repository.places_fr'
        db.delete_column('portal_repository', 'places_fr')

        # Deleting field 'Repository.buildings_en'
        db.delete_column('portal_repository', 'buildings_en')


    def backwards(self, orm):
        
        # Adding field 'Contact.contact_type_fr'
        db.add_column('portal_contact', 'contact_type_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.contact_type_de'
        db.add_column('portal_contact', 'contact_type_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.note_fr'
        db.add_column('portal_contact', 'note_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Contact.city_fr'
        db.add_column('portal_contact', 'city_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.contact_type_en'
        db.add_column('portal_contact', 'contact_type_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.region_fr'
        db.add_column('portal_contact', 'region_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.note_de'
        db.add_column('portal_contact', 'note_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Contact.region_de'
        db.add_column('portal_contact', 'region_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.note_en'
        db.add_column('portal_contact', 'note_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Contact.city_en'
        db.add_column('portal_contact', 'city_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.region_en'
        db.add_column('portal_contact', 'region_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Contact.city_de'
        db.add_column('portal_contact', 'city_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_en'
        db.add_column('portal_repository', 'rules_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.internal_structures_de'
        db.add_column('portal_repository', 'internal_structures_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_de'
        db.add_column('portal_repository', 'finding_aids_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.mandates_de'
        db.add_column('portal_repository', 'mandates_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.functions_en'
        db.add_column('portal_repository', 'functions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_en'
        db.add_column('portal_repository', 'dates_of_existence_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.places_de'
        db.add_column('portal_repository', 'places_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.history_de'
        db.add_column('portal_repository', 'history_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_de'
        db.add_column('portal_repository', 'collecting_policies_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_fr'
        db.add_column('portal_repository', 'disabled_access_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.internal_structures_en'
        db.add_column('portal_repository', 'internal_structures_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.legal_status_de'
        db.add_column('portal_repository', 'legal_status_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_de'
        db.add_column('portal_repository', 'rules_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.maintenance_notes_fr'
        db.add_column('portal_repository', 'maintenance_notes_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.functions_de'
        db.add_column('portal_repository', 'functions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.history_en'
        db.add_column('portal_repository', 'history_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.holdings_fr'
        db.add_column('portal_repository', 'holdings_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_en'
        db.add_column('portal_repository', 'disabled_access_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.places_en'
        db.add_column('portal_repository', 'places_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.sources_de'
        db.add_column('portal_repository', 'sources_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.maintenance_notes_en'
        db.add_column('portal_repository', 'maintenance_notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_fr'
        db.add_column('portal_repository', 'buildings_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.general_context_de'
        db.add_column('portal_repository', 'general_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.history_fr'
        db.add_column('portal_repository', 'history_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.legal_status_fr'
        db.add_column('portal_repository', 'legal_status_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_fr'
        db.add_column('portal_repository', 'rules_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_fr'
        db.add_column('portal_repository', 'opening_times_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_en'
        db.add_column('portal_repository', 'finding_aids_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.maintenance_notes_de'
        db.add_column('portal_repository', 'maintenance_notes_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.mandates_en'
        db.add_column('portal_repository', 'mandates_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_de'
        db.add_column('portal_repository', 'dates_of_existence_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.general_context_en'
        db.add_column('portal_repository', 'general_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_en'
        db.add_column('portal_repository', 'collecting_policies_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_en'
        db.add_column('portal_repository', 'opening_times_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.holdings_en'
        db.add_column('portal_repository', 'holdings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_fr'
        db.add_column('portal_repository', 'research_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_de'
        db.add_column('portal_repository', 'geocultural_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_en'
        db.add_column('portal_repository', 'reproduction_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.general_context_fr'
        db.add_column('portal_repository', 'general_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_de'
        db.add_column('portal_repository', 'buildings_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_de'
        db.add_column('portal_repository', 'opening_times_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_fr'
        db.add_column('portal_repository', 'dates_of_existence_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_fr'
        db.add_column('portal_repository', 'access_conditions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_de'
        db.add_column('portal_repository', 'reproduction_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.internal_structures_fr'
        db.add_column('portal_repository', 'internal_structures_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_de'
        db.add_column('portal_repository', 'research_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.legal_status_en'
        db.add_column('portal_repository', 'legal_status_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_en'
        db.add_column('portal_repository', 'access_conditions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_fr'
        db.add_column('portal_repository', 'finding_aids_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.mandates_fr'
        db.add_column('portal_repository', 'mandates_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_fr'
        db.add_column('portal_repository', 'geocultural_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_de'
        db.add_column('portal_repository', 'disabled_access_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.sources_en'
        db.add_column('portal_repository', 'sources_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_de'
        db.add_column('portal_repository', 'access_conditions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_fr'
        db.add_column('portal_repository', 'reproduction_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.functions_fr'
        db.add_column('portal_repository', 'functions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_en'
        db.add_column('portal_repository', 'research_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_en'
        db.add_column('portal_repository', 'geocultural_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_fr'
        db.add_column('portal_repository', 'collecting_policies_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.holdings_de'
        db.add_column('portal_repository', 'holdings_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.sources_fr'
        db.add_column('portal_repository', 'sources_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.places_fr'
        db.add_column('portal_repository', 'places_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_en'
        db.add_column('portal_repository', 'buildings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['portal.Repository']"}),
            'street_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'portal.fuzzydate': {
            'Meta': {'object_name': 'FuzzyDate'},
            'circa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dates'", 'to': "orm['portal.Collection']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precision': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True'})
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
            'buildings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dates_of_existence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_access': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geocultural_context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'holdings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'internal_structures': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'maintenance_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'opening_times': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['portal.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['portal']
