# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventRecord'
        db.create_table(u'event_eventrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'event', ['EventRecord'])

        # Adding model 'EventRecordEntry'
        db.create_table(u'event_eventrecordentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.EventRecord'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'event', ['EventRecordEntry'])

        # Adding model 'EventMemo'
        db.create_table(u'event_eventmemo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.EventMemo'])),
            ('memo', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'event', ['EventMemo'])

        # Adding model 'EventFieldChange'
        db.create_table(u'event_eventfieldchange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('new', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'event', ['EventFieldChange'])


    def backwards(self, orm):
        # Deleting model 'EventRecord'
        db.delete_table(u'event_eventrecord')

        # Deleting model 'EventRecordEntry'
        db.delete_table(u'event_eventrecordentry')

        # Deleting model 'EventMemo'
        db.delete_table(u'event_eventmemo')

        # Deleting model 'EventFieldChange'
        db.delete_table(u'event_eventfieldchange')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'event.eventfieldchange': {
            'Meta': {'object_name': 'EventFieldChange'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'event.eventmemo': {
            'Meta': {'object_name': 'EventMemo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.EventMemo']"})
        },
        u'event.eventrecord': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'EventRecord'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'event.eventrecordentry': {
            'Meta': {'object_name': 'EventRecordEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.EventRecord']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['event']