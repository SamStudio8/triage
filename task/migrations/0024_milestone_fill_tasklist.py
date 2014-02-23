# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        User = orm['auth.User']
        for user in User.objects.all():
            old_milestones = []
            for tasklist in orm.TaskList.objects.filter(user__id=user.pk):
                milestones = []

                # List all milestones attached to at least one task in tasklist
                for task in tasklist.tasks.all():
                    if task.milestone:
                        m = task.milestone
                        if m not in milestones:
                            milestones.append(m)

                for milestone in milestones:
                    old_milestone_pk = milestone.pk
                    old_milestones.append(old_milestone_pk)

                    # Clone old milestone and attach it to the current tasklist
                    milestone.pk = None
                    milestone.tasklist = tasklist
                    milestone.save()

                    # Point tasks in the current tasklist attached to the
                    # "old milestone" to shiny new list-owned milestone
                    for task in orm.Task.objects.filter(tasklist__id=tasklist.pk,
                                                        milestone__id=old_milestone_pk):
                        task.milestone = milestone
                        task.save()

            # Remove the old milestones
            for old_pk in old_milestones:
                orm.TaskMilestone.objects.filter(id=old_pk).delete()

    def backwards(self, orm):
        #TODO Nuke duplicates
        for milestone in orm.TaskMilestone.objects.all():
            milestone.tasklist = None
            milestone.save()


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
            'Meta': {'ordering': "['completed', 'due_date', '-triage__priority']", 'object_name': 'Task'},
            '_id': ('django.db.models.fields.IntegerField', [], {}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskMilestone']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tasklist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['task.TaskList']"}),
            'triage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskTriageCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'task.tasklink': {
            'Meta': {'unique_together': "(('from_task', 'to_task'),)", 'object_name': 'TaskLink'},
            'from_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links_out'", 'to': u"orm['task.Task']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskLinkType']"}),
            'to_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links_in'", 'to': u"orm['task.Task']"})
        },
        u'task.tasklinktype': {
            'Meta': {'object_name': 'TaskLinkType'},
            'from_desc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'to_desc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'task.tasklist': {
            'Meta': {'ordering': "['-order']", 'unique_together': "(('user', 'slug'),)", 'object_name': 'TaskList'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasklists'", 'to': u"orm['auth.User']"})
        },
        u'task.taskmilestone': {
            'Meta': {'ordering': "['-due_date']", 'object_name': 'TaskMilestone'},
            'bg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'tasklist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskList']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': u"orm['auth.User']"})
        },
        u'task.tasktriagecategory': {
            'Meta': {'ordering': "['-priority']", 'object_name': 'TaskTriageCategory'},
            'bg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'fg_colour': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'triages'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['task']
    symmetrical = True