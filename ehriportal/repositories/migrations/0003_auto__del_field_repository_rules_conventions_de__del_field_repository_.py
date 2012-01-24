# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Repository.rules_conventions_de'
        db.delete_column('repositories_repository', 'rules_conventions_de')

        # Deleting field 'Repository.rules_conventions_fr'
        db.delete_column('repositories_repository', 'rules_conventions_fr')

        # Deleting field 'Repository.rules_conventions_en'
        db.delete_column('repositories_repository', 'rules_conventions_en')

        # Deleting field 'Repository.rules_conventions'
        db.delete_column('repositories_repository', 'rules_conventions')

        # Adding field 'Repository.access_conditions'
        db.add_column('repositories_repository', 'access_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_en'
        db.add_column('repositories_repository', 'access_conditions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_de'
        db.add_column('repositories_repository', 'access_conditions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.access_conditions_fr'
        db.add_column('repositories_repository', 'access_conditions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings'
        db.add_column('repositories_repository', 'buildings', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_en'
        db.add_column('repositories_repository', 'buildings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_de'
        db.add_column('repositories_repository', 'buildings_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.buildings_fr'
        db.add_column('repositories_repository', 'buildings_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies'
        db.add_column('repositories_repository', 'collecting_policies', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_en'
        db.add_column('repositories_repository', 'collecting_policies_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_de'
        db.add_column('repositories_repository', 'collecting_policies_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.collecting_policies_fr'
        db.add_column('repositories_repository', 'collecting_policies_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_en'
        db.add_column('repositories_repository', 'dates_of_existence_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_de'
        db.add_column('repositories_repository', 'dates_of_existence_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.dates_of_existence_fr'
        db.add_column('repositories_repository', 'dates_of_existence_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access'
        db.add_column('repositories_repository', 'disabled_access', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_en'
        db.add_column('repositories_repository', 'disabled_access_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_de'
        db.add_column('repositories_repository', 'disabled_access_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.disabled_access_fr'
        db.add_column('repositories_repository', 'disabled_access_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids'
        db.add_column('repositories_repository', 'finding_aids', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_en'
        db.add_column('repositories_repository', 'finding_aids_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_de'
        db.add_column('repositories_repository', 'finding_aids_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.finding_aids_fr'
        db.add_column('repositories_repository', 'finding_aids_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context'
        db.add_column('repositories_repository', 'geocultural_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_en'
        db.add_column('repositories_repository', 'geocultural_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_de'
        db.add_column('repositories_repository', 'geocultural_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.geocultural_context_fr'
        db.add_column('repositories_repository', 'geocultural_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times'
        db.add_column('repositories_repository', 'opening_times', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_en'
        db.add_column('repositories_repository', 'opening_times_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_de'
        db.add_column('repositories_repository', 'opening_times_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.opening_times_fr'
        db.add_column('repositories_repository', 'opening_times_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services'
        db.add_column('repositories_repository', 'reproduction_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_en'
        db.add_column('repositories_repository', 'reproduction_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_de'
        db.add_column('repositories_repository', 'reproduction_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.reproduction_services_fr'
        db.add_column('repositories_repository', 'reproduction_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services'
        db.add_column('repositories_repository', 'research_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_en'
        db.add_column('repositories_repository', 'research_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_de'
        db.add_column('repositories_repository', 'research_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.research_services_fr'
        db.add_column('repositories_repository', 'research_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules'
        db.add_column('repositories_repository', 'rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_en'
        db.add_column('repositories_repository', 'rules_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_de'
        db.add_column('repositories_repository', 'rules_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_fr'
        db.add_column('repositories_repository', 'rules_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Repository.rules_conventions_de'
        db.add_column('repositories_repository', 'rules_conventions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_conventions_fr'
        db.add_column('repositories_repository', 'rules_conventions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_conventions_en'
        db.add_column('repositories_repository', 'rules_conventions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Repository.rules_conventions'
        db.add_column('repositories_repository', 'rules_conventions', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Repository.access_conditions'
        db.delete_column('repositories_repository', 'access_conditions')

        # Deleting field 'Repository.access_conditions_en'
        db.delete_column('repositories_repository', 'access_conditions_en')

        # Deleting field 'Repository.access_conditions_de'
        db.delete_column('repositories_repository', 'access_conditions_de')

        # Deleting field 'Repository.access_conditions_fr'
        db.delete_column('repositories_repository', 'access_conditions_fr')

        # Deleting field 'Repository.buildings'
        db.delete_column('repositories_repository', 'buildings')

        # Deleting field 'Repository.buildings_en'
        db.delete_column('repositories_repository', 'buildings_en')

        # Deleting field 'Repository.buildings_de'
        db.delete_column('repositories_repository', 'buildings_de')

        # Deleting field 'Repository.buildings_fr'
        db.delete_column('repositories_repository', 'buildings_fr')

        # Deleting field 'Repository.collecting_policies'
        db.delete_column('repositories_repository', 'collecting_policies')

        # Deleting field 'Repository.collecting_policies_en'
        db.delete_column('repositories_repository', 'collecting_policies_en')

        # Deleting field 'Repository.collecting_policies_de'
        db.delete_column('repositories_repository', 'collecting_policies_de')

        # Deleting field 'Repository.collecting_policies_fr'
        db.delete_column('repositories_repository', 'collecting_policies_fr')

        # Deleting field 'Repository.dates_of_existence_en'
        db.delete_column('repositories_repository', 'dates_of_existence_en')

        # Deleting field 'Repository.dates_of_existence_de'
        db.delete_column('repositories_repository', 'dates_of_existence_de')

        # Deleting field 'Repository.dates_of_existence_fr'
        db.delete_column('repositories_repository', 'dates_of_existence_fr')

        # Deleting field 'Repository.disabled_access'
        db.delete_column('repositories_repository', 'disabled_access')

        # Deleting field 'Repository.disabled_access_en'
        db.delete_column('repositories_repository', 'disabled_access_en')

        # Deleting field 'Repository.disabled_access_de'
        db.delete_column('repositories_repository', 'disabled_access_de')

        # Deleting field 'Repository.disabled_access_fr'
        db.delete_column('repositories_repository', 'disabled_access_fr')

        # Deleting field 'Repository.finding_aids'
        db.delete_column('repositories_repository', 'finding_aids')

        # Deleting field 'Repository.finding_aids_en'
        db.delete_column('repositories_repository', 'finding_aids_en')

        # Deleting field 'Repository.finding_aids_de'
        db.delete_column('repositories_repository', 'finding_aids_de')

        # Deleting field 'Repository.finding_aids_fr'
        db.delete_column('repositories_repository', 'finding_aids_fr')

        # Deleting field 'Repository.geocultural_context'
        db.delete_column('repositories_repository', 'geocultural_context')

        # Deleting field 'Repository.geocultural_context_en'
        db.delete_column('repositories_repository', 'geocultural_context_en')

        # Deleting field 'Repository.geocultural_context_de'
        db.delete_column('repositories_repository', 'geocultural_context_de')

        # Deleting field 'Repository.geocultural_context_fr'
        db.delete_column('repositories_repository', 'geocultural_context_fr')

        # Deleting field 'Repository.opening_times'
        db.delete_column('repositories_repository', 'opening_times')

        # Deleting field 'Repository.opening_times_en'
        db.delete_column('repositories_repository', 'opening_times_en')

        # Deleting field 'Repository.opening_times_de'
        db.delete_column('repositories_repository', 'opening_times_de')

        # Deleting field 'Repository.opening_times_fr'
        db.delete_column('repositories_repository', 'opening_times_fr')

        # Deleting field 'Repository.reproduction_services'
        db.delete_column('repositories_repository', 'reproduction_services')

        # Deleting field 'Repository.reproduction_services_en'
        db.delete_column('repositories_repository', 'reproduction_services_en')

        # Deleting field 'Repository.reproduction_services_de'
        db.delete_column('repositories_repository', 'reproduction_services_de')

        # Deleting field 'Repository.reproduction_services_fr'
        db.delete_column('repositories_repository', 'reproduction_services_fr')

        # Deleting field 'Repository.research_services'
        db.delete_column('repositories_repository', 'research_services')

        # Deleting field 'Repository.research_services_en'
        db.delete_column('repositories_repository', 'research_services_en')

        # Deleting field 'Repository.research_services_de'
        db.delete_column('repositories_repository', 'research_services_de')

        # Deleting field 'Repository.research_services_fr'
        db.delete_column('repositories_repository', 'research_services_fr')

        # Deleting field 'Repository.rules'
        db.delete_column('repositories_repository', 'rules')

        # Deleting field 'Repository.rules_en'
        db.delete_column('repositories_repository', 'rules_en')

        # Deleting field 'Repository.rules_de'
        db.delete_column('repositories_repository', 'rules_de')

        # Deleting field 'Repository.rules_fr'
        db.delete_column('repositories_repository', 'rules_fr')


    models = {
        'repositories.contact': {
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'region_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['repositories.Repository']"}),
            'street_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'repositories.othername': {
            'Meta': {'object_name': 'OtherName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_names'", 'to': "orm['repositories.Repository']"})
        },
        'repositories.repository': {
            'Meta': {'object_name': 'Repository'},
            'access_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_conditions_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'authorized_form_of_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'buildings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'buildings_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collecting_policies_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'internal_structures': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'internal_structures_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['repositories']
