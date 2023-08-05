# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'MutexModel', fields ['mutex_mode']
        db.create_index('m3_mutex', ['mutex_mode'])

        # Adding index on 'MutexModel', fields ['mutex_id']
        db.create_index('m3_mutex', ['mutex_id'])

        # Adding index on 'MutexModel', fields ['mutex_group']
        db.create_index('m3_mutex', ['mutex_group'])


    def backwards(self, orm):
        # Removing index on 'MutexModel', fields ['mutex_group']
        db.delete_index('m3_mutex', ['mutex_group'])

        # Removing index on 'MutexModel', fields ['mutex_id']
        db.delete_index('m3_mutex', ['mutex_id'])

        # Removing index on 'MutexModel', fields ['mutex_mode']
        db.delete_index('m3_mutex', ['mutex_mode'])


    models = {
        u'm3_mutex.mutexmodel': {
            'Meta': {'object_name': 'MutexModel', 'db_table': "'m3_mutex'"},
            'auto_release_config': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'auto_release_rule': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'captured_since': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutex_group': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'mutex_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'mutex_mode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'owner_host': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner_id': ('django.db.models.fields.CharField', [], {'default': "'system'", 'max_length': '40'}),
            'owner_login': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'owner_session': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['m3_mutex']