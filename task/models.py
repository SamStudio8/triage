import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc

from event import models as EventModels

class Task(models.Model):
    _id = models.IntegerField()
    tasklist = models.ForeignKey('TaskList',
                                related_name='tasks')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    triage = models.ForeignKey('TaskTriageCategory',
                               null=True,
                               blank=True)
#    status = models.ForeignKey('TaskStatus')
    progress = models.IntegerField(default=0)

    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    due_date = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField()
    completed_date = models.DateTimeField(null=True, blank=True)

    RECORD_OPTIONS = {
        "invisible": [ "modified_date" ],
        "no_expand": [ "description" ]
    }

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

    @property
    def user_id(self):
        return self.tasklist.user_id

    @property
    def local_id(self):
        return self._id

    # Update timestamps and assign _id
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.datetime.utcnow().replace(tzinfo=utc)

            tasks = Task.objects.filter(tasklist__user__id=self.tasklist.user.pk)
            if len(tasks) == 0:
                self._id = 1
            else:
                first = tasks.order_by("-id")[0]
                self._id = first.pk + 1

        self.modified_date = datetime.datetime.utcnow().replace(tzinfo=utc)
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

#class TaskStatus(models.Model):
#    user = models.ForeignKey(User)
#    name = models.CharField(max_length=30)
#    description = models.CharField(max_length=255, blank=True)
#    is_closed = models.BooleanField()

#    def __unicode__(self):
#        return self.name

class TaskList(models.Model):
    user = models.ForeignKey(User,
                            verbose_name="owner",
                            related_name="tasklists")
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class TaskLinkType(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    from_desc = models.CharField(max_length=30)
    to_desc = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class TaskLink(models.Model):
    from_task = models.ForeignKey(Task, related_name="links_out")
    to_task = models.ForeignKey(Task, related_name="links_in")
    link_type = models.ForeignKey(TaskLinkType)

    class Meta:
        unique_together = ("from_task", "to_task")

