# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Resource'
        db.create_table('portal_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['Resource'])

        # Adding model 'ResourceImage'
        db.create_table('portal_resourceimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Resource'])),
            ('image', self.gf('portal.thumbs.ImageWithThumbsField')(max_length=100, name='image', sizes=((100, 100), (300, 300)))),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['ResourceImage'])

        # Adding model 'OtherName'
        db.create_table('portal_othername', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Resource'])),
        ))
        db.send_create_signal('portal', ['OtherName'])

        # Adding model 'Property'
        db.create_table('portal_property', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Resource'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('portal', ['Property'])

        # Adding model 'Place'
        db.create_table('portal_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Resource'])),
        ))
        db.send_create_signal('portal', ['Place'])

        # Adding model 'Repository'
        db.create_table('portal_repository', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['portal.Resource'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=(), db_index=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('logo', self.gf('portal.thumbs.ImageWithThumbsField')(name='logo', sizes=((100, 100), (300, 300)), max_length=100, blank=True, null=True)),
            ('access_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('buildings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collecting_policies', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dates_of_existence', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('disabled_access', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geocultural_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('holdings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opening_times', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('research_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['Repository'])

        # Adding model 'Contact'
        db.create_table('portal_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['portal.Repository'])),
            ('contact_person', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('street_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['Contact'])

        # Adding model 'Collection'
        db.create_table('portal_collection', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['portal.Resource'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=(), db_index=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Repository'])),
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
        db.send_create_signal('portal', ['Collection'])

        # Adding model 'FuzzyDate'
        db.create_table('portal_fuzzydate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dates', to=orm['portal.Collection'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('precision', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('circa', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('portal', ['FuzzyDate'])


    def backwards(self, orm):
        
        # Deleting model 'Resource'
        db.delete_table('portal_resource')

        # Deleting model 'ResourceImage'
        db.delete_table('portal_resourceimage')

        # Deleting model 'OtherName'
        db.delete_table('portal_othername')

        # Deleting model 'Property'
        db.delete_table('portal_property')

        # Deleting model 'Place'
        db.delete_table('portal_place')

        # Deleting model 'Repository'
        db.delete_table('portal_repository')

        # Deleting model 'Contact'
        db.delete_table('portal_contact')

        # Deleting model 'Collection'
        db.delete_table('portal_collection')

        # Deleting model 'FuzzyDate'
        db.delete_table('portal_fuzzydate')


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
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'institution_responsible_identifier': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_copies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location_of_originals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'physical_characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_units_of_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portal.Repository']"}),
            'reproduction_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['portal.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'revision_history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'scope_and_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
        'portal.place': {
            'Meta': {'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'internal_structures': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo': ('portal.thumbs.ImageWithThumbsField', [], {'name': "'logo'", 'sizes': '((100, 100), (300, 300))', 'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'maintenance_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mandates': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opening_times': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'places': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reproduction_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['portal.Resource']", 'unique': 'True', 'primary_key': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'portal.resource': {
            'Meta': {'object_name': 'Resource'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'portal.resourceimage': {
            'Meta': {'object_name': 'ResourceImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('portal.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'name': "'image'", 'sizes': '((100, 100), (300, 300))'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portal.Resource']"})
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
