import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc

class Task(models.Model):

    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='subtasks')
    tasklist = models.ForeignKey('TaskList',
                                related_name='tasks')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    priority = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    due_date = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField()

    # Update timestamps
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.modified_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(Task, self).save(*args, **kwargs)

class TaskList(models.Model):
    # Future; Colour Coded
    user = models.ForeignKey(User,
                            verbose_name="owner",
                            related_name="tasklists")
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True)

class TaskTarget(models.Model):
    pass

class TaskGoal(models.Model):
    pass
