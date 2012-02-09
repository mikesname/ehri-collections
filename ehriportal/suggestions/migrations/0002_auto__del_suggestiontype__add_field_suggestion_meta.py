# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'SuggestionType'
        db.delete_table('suggestions_suggestiontype')

        # Adding field 'Suggestion.meta'
        db.add_column('suggestions_suggestion', 'meta', self.gf('jsonfield.fields.JSONField')(null=True), keep_default=False)

        # Removing M2M table for field types on 'Suggestion'
        db.delete_table('suggestions_suggestion_types')


    def backwards(self, orm):
        
        # Adding model 'SuggestionType'
        db.create_table('suggestions_suggestiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('suggestions', ['SuggestionType'])

        # Deleting field 'Suggestion.meta'
        db.delete_column('suggestions_suggestion', 'meta')

        # Adding M2M table for field types on 'Suggestion'
        db.create_table('suggestions_suggestion_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('suggestion', models.ForeignKey(orm['suggestions.suggestion'], null=False)),
            ('suggestiontype', models.ForeignKey(orm['suggestions.suggestiontype'], null=False))
        ))
        db.create_unique('suggestions_suggestion_types', ['suggestion_id', 'suggestiontype_id'])


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
