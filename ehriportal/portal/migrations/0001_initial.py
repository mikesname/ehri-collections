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
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=(), db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lod', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_of_entity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['Resource'])

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

        # Adding model 'Repository'
        db.create_table('portal_repository', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['portal.Resource'], unique=True, primary_key=True)),
            ('access_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('access_conditions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('access_conditions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('access_conditions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('buildings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('buildings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('buildings_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('buildings_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collecting_policies', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collecting_policies_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collecting_policies_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collecting_policies_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dates_of_existence', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dates_of_existence_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dates_of_existence_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dates_of_existence_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('disabled_access', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('disabled_access_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('disabled_access_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('disabled_access_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('finding_aids_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('functions_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('general_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geocultural_context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geocultural_context_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geocultural_context_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geocultural_context_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('holdings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('holdings_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('holdings_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('holdings_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('internal_structures_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('legal_status_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('maintenance_notes_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mandates_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opening_times', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opening_times_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opening_times_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('opening_times_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('places_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reproduction_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('research_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('research_services_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('research_services_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('research_services_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rules_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
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
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contact_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_type_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_type_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('contact_type_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('region_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('region_de', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('region_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('portal', ['Contact'])

        # Adding model 'Collection'
        db.create_table('portal_collection', (
            ('resource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['portal.Resource'], unique=True, primary_key=True)),
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


    def backwards(self, orm):
        
        # Deleting model 'Resource'
        db.delete_table('portal_resource')

        # Deleting model 'OtherName'
        db.delete_table('portal_othername')

        # Deleting model 'Property'
        db.delete_table('portal_property')

        # Deleting model 'Repository'
        db.delete_table('portal_repository')

        # Deleting model 'Contact'
        db.delete_table('portal_contact')

        # Deleting model 'Collection'
        db.delete_table('portal_collection')


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
            'lod': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['portal']
