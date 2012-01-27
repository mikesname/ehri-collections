# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ArchivalResource'
        db.create_table('archival_resource_archivalresource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=(), db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('archival_resource', ['ArchivalResource'])

        # Adding model 'OtherName'
        db.create_table('archival_resource_othername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archival_resource.ArchivalResource'])),
        ))
        db.send_create_signal('archival_resource', ['OtherName'])

        # Adding model 'Property'
        db.create_table('archival_resource_property', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archival_resource.ArchivalResource'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('archival_resource', ['Property'])


    def backwards(self, orm):
        
        # Deleting model 'ArchivalResource'
        db.delete_table('archival_resource_archivalresource')

        # Deleting model 'OtherName'
        db.delete_table('archival_resource_othername')

        # Deleting model 'Property'
        db.delete_table('archival_resource_property')


    models = {
        'archival_resource.archivalresource': {
            'Meta': {'object_name': 'ArchivalResource'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'archival_resource.othername': {
            'Meta': {'object_name': 'OtherName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archival_resource.ArchivalResource']"})
        },
        'archival_resource.property': {
            'Meta': {'object_name': 'Property'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archival_resource.ArchivalResource']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['archival_resource']
