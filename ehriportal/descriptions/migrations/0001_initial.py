# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Description'
        db.create_table('descriptions_description', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repositories.Repository'])),
            ('access_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accruals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('acquisition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('alternate_title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('appraisal', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('archival_history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('arrangement', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('extent_and_medium', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('institution_responsible_identifier', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location_of_copies', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location_of_originals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('physical_characteristics', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('related_units_of_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('revision_history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('scope_and_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('descriptions', ['Description'])

        # Adding model 'OtherName'
        db.create_table('descriptions_othername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['descriptions.Description'])),
        ))
        db.send_create_signal('descriptions', ['OtherName'])


    def backwards(self, orm):
        
        # Deleting model 'Description'
        db.delete_table('descriptions_description')

        # Deleting model 'OtherName'
        db.delete_table('descriptions_othername')


    models = {
        'descriptions.description': {
            'Meta': {'object_name': 'Description'},
            'access_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'accruals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'acquisition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alternate_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'appraisal': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'archival_history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'arrangement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'edition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent_and_medium': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finding_aids': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'institution_responsible_identifier': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_copies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_originals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'physical_characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_units_of_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repositories.Repository']"}),
            'reproduction_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'revision_history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'scope_and_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'descriptions.othername': {
            'Meta': {'object_name': 'OtherName'},
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['descriptions.Description']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
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
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['descriptions']
