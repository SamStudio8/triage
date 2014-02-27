import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.utils.timezone import utc

import event.models as EventModels
import event.utils as EventUtils

class Task(models.Model):
    _id = models.IntegerField()
    tasklist = models.ForeignKey('TaskList',
                                related_name='tasks')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,
            help_text=("Description allows Markdown input"))

    triage = models.ForeignKey('TaskTriageCategory',
                               null=True,
                               blank=True)
    milestone = models.ForeignKey('TaskMilestone',
                               null=True,
                               blank=True)
#    status = models.ForeignKey('TaskStatus')

    due_date = models.DateTimeField(null=True, blank=True)

    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    completed = models.BooleanField()
    completed_date = models.DateTimeField(null=True, blank=True)

    RECORD_OPTIONS = {
        "insignificant": [ "modified_date" ],
        "invisible": [ "modified_date" ],
        "no_expand": [ "description" ]
    }

    class Meta:
        ordering = ["completed", "due_date", "-triage__priority"]

    def __unicode__(self):
        return "#%d %s" % (self.local_id, self.name)

    def has_view_permission(self, uid):
        if self.tasklist.public:
            return True
        else:
            return uid == self.tasklist.user.pk

    def has_edit_permission(self, uid):
          return uid == self.tasklist.user.pk

    @property
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
    def created_by(self):
        try:
            return EventUtils._get_history(self)[0].user
        except IndexError:
            return None

    @property
    def modified_by(self):
        try:
            return EventUtils._get_history(self).reverse()[0].user
        except IndexError:
            return None

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
                self._id = first._id + 1

        self.modified_date = datetime.datetime.utcnow().replace(tzinfo=utc)

        if self.completed:
            self.completed_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        else:
            self.completed_date = None

        # Remove milestone if list doesn't contain it
        if self.id:
            #TODO This would be a bit inefficient if users had a crazy number
            #     of milestones in the given tasklist
            if self.milestone not in self.tasklist.milestones.all():
                self.milestone = None

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

    class Meta:
        ordering = ["-priority"]

    def open_tasks(self):
        return self.task_set.annotate(null=Count("due_date")).filter(completed=False).order_by("-null", "due_date", "-triage__priority")

    def closed_tasks(self):
        return self.task_set.filter(completed=True).order_by("-completed_date")

class TaskMilestone(models.Model):
    tasklist = models.ForeignKey('TaskList',
                                related_name='milestones',
                                null=True, blank=True)
    name = models.CharField(max_length=30)
    due_date = models.DateTimeField(null=True, blank=True)
    fg_colour = models.CharField(max_length=6)
    bg_colour = models.CharField(max_length=6)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-due_date"]

    def has_view_permission(self, uid):
        if self.tasklist.public:
            return True
        else:
            return uid == self.tasklist.user.pk

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
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0,
            help_text=("Use to change the order in which your lists appear. "
                "Higher numbers will take priority."))
    public = models.BooleanField(default=False,
            help_text=("Share this tasklist publicly - ALL TASKS WILL BE VISIBLE TO ANYONE"))

    def __unicode__(self):
        return self.name

    def has_view_permission(self, uid):
        if self.public:
            return True
        else:
            return uid == self.user.pk

    def has_edit_permission(self, uid):
          return uid == self.user.pk

    def open_tasks(self):
        return self.tasks.annotate(null=Count("due_date")).filter(completed=False).order_by("-null", "due_date", "-triage__priority")

    def closed_tasks(self):
        return self.tasks.filter(completed=True).order_by("-completed_date")

    def upcoming_tasks(self, offset=0, days=7):
        today = datetime.datetime.utcnow().replace(tzinfo=utc)
        offset_date = today + datetime.timedelta(days=offset)
        delta_date = today + datetime.timedelta(days=days+offset)

        return self.tasks.filter(completed=False, due_date__range=[offset_date, delta_date]).order_by("-triage__priority", "due_date")

    def overdue_tasks(self):
        today = datetime.datetime.utcnow().replace(tzinfo=utc)
        return self.tasks.filter(completed=False, due_date__lte=today).order_by("-due_date")

    def recently_closed(self, limit=None):
        return self.tasks.filter(completed=True).order_by("completed_date")[:limit].reverse()

    def recently_added(self, limit=None):
        return self.tasks.order_by("creation_date")[:limit].reverse()

    @property
    def num_incomplete(self):
        return self.tasks.filter(completed=False).count()

    @property
    def num_complete(self):
        return self.tasks.filter(completed=True).count()

    class Meta:
        ordering = ["-order"]
        unique_together = ("user", "slug")

    # Update slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TaskList, self).save(*args, **kwargs)

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

