# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Story.lat'
        db.add_column('wanted_story', 'lat', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'Story.lng'
        db.add_column('wanted_story', 'lng', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Story.lat'
        db.delete_column('wanted_story', 'lat')

        # Deleting field 'Story.lng'
        db.delete_column('wanted_story', 'lng')


    models = {
        'wanted.story': {
            'Meta': {'object_name': 'Story'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['wanted']
