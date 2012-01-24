# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Repository'
        db.create_table('repositories_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('authorized_form_of_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dates_of_existence', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_conventions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_conventions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_conventions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_conventions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repositories', ['Repository'])

        # Adding model 'OtherName'
        db.create_table('repositories_othername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(related_name='other_names', to=orm['repositories.Repository'])),
        ))
        db.send_create_signal('repositories', ['OtherName'])


    def backwards(self, orm):
        
        # Deleting model 'Repository'
        db.delete_table('repositories_repository')

        # Deleting model 'OtherName'
        db.delete_table('repositories_othername')


    models = {
        'repositories.othername': {
            'Meta': {'object_name': 'OtherName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_names'", 'to': "orm['repositories.Repository']"})
        },
        'repositories.repository': {
            'Meta': {'object_name': 'Repository'},
            'authorized_form_of_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dates_of_existence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'functions_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'general_context_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'places': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_conventions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_conventions_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_conventions_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_conventions_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sources_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['repositories']
