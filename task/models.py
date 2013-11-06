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

    triage = models.ForeignKey('TaskTriageCategory',
                               null=True,
                               blank=True)
    progress = models.IntegerField(default=0)

    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    due_date = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField()
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["completed", "due_date", "-triage__priority"]

    def __unicode__(self):
        return "#%d %s" % (self.id, self.name)

    def is_due(self):
        if self.due_date == self.modified_date:
            return 0

        if self.due_date < datetime.datetime.utcnow().replace(tzinfo=utc):
            # Overdue
            return -1
        elif self.due_date.date() == self.due_date.today().date():
            # Today
            return 1
        else:
            # OK
            return 0

    # Update timestamps
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.modified_date = datetime.datetime.utcnow().replace(tzinfo=utc)

        if not self.completed and not self.due_date:
            # Update the due date to now if the task is not completed yet
            #TODO Future: User preference as to how to order due_date of None
            self.due_date = self.modified_date
        super(Task, self).save(*args, **kwargs)

class TaskTriageCategory(models.Model):
    user = models.ForeignKey(User,
                            verbose_name="owner",
                            related_name="triages")
    name = models.CharField(max_length=30)
    priority = models.IntegerField(default=0)
    fg_colour = models.CharField(max_length=6)
    bg_colour = models.CharField(max_length=6)

    def __unicode__(self):
        return self.name

class TaskList(models.Model):
    # Future; Colour Coded
    user = models.ForeignKey(User,
                            verbose_name="owner",
                            related_name="tasklists")
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class TaskTarget(models.Model):
    pass

class TaskGoal(models.Model):
    pass
