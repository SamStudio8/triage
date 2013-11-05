# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'task_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subtasks', null=True, to=orm['task.Task'])),
            ('tasklist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['task.TaskList'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('triage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.TaskTriageCategory'], null=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'task', ['Task'])

        # Adding model 'TaskTriageCategory'
        db.create_table(u'task_tasktriagecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fg_colour', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('bg_colour', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'task', ['TaskTriageCategory'])

        # Adding model 'TaskList'
        db.create_table(u'task_tasklist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasklists', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'task', ['TaskList'])

        # Adding model 'TaskTarget'
        db.create_table(u'task_tasktarget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'task', ['TaskTarget'])

        # Adding model 'TaskGoal'
        db.create_table(u'task_taskgoal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'task', ['TaskGoal'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'task_task')

        # Deleting model 'TaskTriageCategory'
        db.delete_table(u'task_tasktriagecategory')

        # Deleting model 'TaskList'
        db.delete_table(u'task_tasklist')

        # Deleting model 'TaskTarget'
        db.delete_table(u'task_tasktarget')

        # Deleting model 'TaskGoal'
        db.delete_table(u'task_taskgoal')


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
        u'task.task': {
            'Meta': {'ordering': "['completed', 'due_date']", 'object_name': 'Task'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subtasks'", 'null': 'True', 'to': u"orm['task.Task']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'progress': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tasklist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['task.TaskList']"}),
            'triage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskTriageCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'task.taskgoal': {
            'Meta': {'object_name': 'TaskGoal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'task.tasklist': {
            'Meta': {'object_name': 'TaskList'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasklists'", 'to': u"orm['auth.User']"})
        },
        u'task.tasktarget': {
            'Meta': {'object_name': 'TaskTarget'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'task.tasktriagecategory': {
            'Meta': {'object_name': 'TaskTriageCategory'},
            'bg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'fg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['task']