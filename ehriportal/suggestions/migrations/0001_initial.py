# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Suggestion'
        db.create_table('suggestions_suggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('meta', self.gf('jsonfield.fields.JSONField')(null=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('suggestions', ['Suggestion'])


    def backwards(self, orm):
        
        # Deleting model 'Suggestion'
        db.delete_table('suggestions_suggestion')


    models = {
        'suggestions.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['suggestions']
