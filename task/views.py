import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.fields.related import ForeignKey
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.timezone import utc

import task.models as TaskModels
import task.forms as TaskForms
import task.utils as TaskUtils
import task.events as TaskEvents
import event.utils as EventUtils

@login_required
def list_tasks(request):
    tasklists = request.user.tasklists.all()
    return render(request, "task/list.html", {"tasklists": tasklists})

@login_required
def new_task(request, username, listslug=None):
    if listslug:
        tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
        if tasklist.has_permission(request.user.pk):
            return edit_task(request, username, None, tasklist.pk)
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return edit_task(request, username, None, None)

def view_tasklist(request, username, listslug):
    tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
    if not tasklist.has_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))
    calendar = TaskUtils.calendarize(request.user.pk, 30, tasklist.pk)
    return render(request, "task/tasklist.html", {"tasklist": tasklist, "calendar": calendar})

def view_task(request, username, task_id):
    task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
    if not task.has_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))
    history = EventUtils._get_history(task)
    return render(request, "task/view.html", {"task": task, "history": history})

@login_required
def edit_task(request, username, task_id, tasklist_id=None):

    if tasklist_id:
        tasklist = get_object_or_404(TaskModels.TaskList, pk=tasklist_id)
        if not tasklist.has_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))

    task = None
    if task_id:
        try:
            task = TaskModels.Task.objects.get(tasklist__user__username=username, _id=task_id)
        except TaskModels.Task.DoesNotExist:
            pass
        else:
            if not task.has_permission(request.user.pk):
                return HttpResponseRedirect(reverse('home'))
            tasklist_id = task.tasklist_id

    # Fill in POST with data from the model that is not in the request
    post = request.POST or None
    if task and request.method == "POST":
        post = request.POST.copy()
        for field in task._meta.fields:
            attr = field.name
            value = getattr(task, attr)
            if value is not None and isinstance(field, ForeignKey):
                value = value._get_pk_val()
            if attr not in post:
                post[attr] = value

    form = TaskForms.TaskForm(request.user.id, post,
            initial={'tasklist': tasklist_id},
            instance=task)
    if form.is_valid():
        # Don't really like hitting the database for a copy of this but it will
        # more than do for now
        if task:
            original = TaskModels.Task.objects.get(pk=task.pk)
        else:
            original = None

        task = form.save(commit=False)
        task.save()

        # Save the history
        TaskEvents.FieldChange(request, original, task)
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/changetask.html", {"form": form, "task": task})

@login_required
def complete_task(request, username, task_id):
    task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
    if not task.has_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))

    # Don't really like hitting the database for a copy of this but it will
    # more than do for now
    if task:
        original = TaskModels.Task.objects.get(pk=task.pk)
    else:
        original = None

    task.completed = True
    task.completed_date = datetime.datetime.utcnow().replace(tzinfo=utc)
    task.save()

    # Save the history
    TaskEvents.FieldChange(request, original, task)
    return HttpResponseRedirect(reverse('home'))

@login_required
def link_task(request, task_id):
    task = get_object_or_404(TaskModels.Task, pk=task_id)
    if not task.has_permission(request.user.username):
        return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskLinkForm(request.user.id, request.POST or None,
            initial={'from_task': task.pk})

    if form.is_valid():
        link = form.save()
        TaskEvents.LinkChange(request, link)
        return HttpResponseRedirect(reverse('task:view_task', args=(task.pk,)))
    return render(request, "task/changelink.html", {"form": form})

@login_required
def add_tasklist(request, username):
    return edit_tasklist(request, username)

@login_required
def edit_tasklist(request, username=None, listslug=None):
    tasklist = None
    if username and listslug:
        tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
        if not tasklist.has_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskListForm(request.POST or None, instance=tasklist)
    if form.is_valid():
        tasklist = form.save(commit=False)
        if not form.instance.pk:
            # New list, attach user
            tasklist.user = request.user
            tasklist.slug = slugify(form.cleaned_data["name"])
        tasklist.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/changelist.html", {"form": form, "tasklist": tasklist})

@login_required
def list_triage_category(request, username):
    triages = request.user.triages.all()
    return render(request, "task/triages.html", {"triages": triages})

@login_required
def list_milestones(request, username):
    milestones = request.user.milestones.all()
    return render(request, "task/milestones.html", {"milestones": milestones})

@login_required
def new_milestone(request, username):
    return edit_milestone(request, None)

@login_required
def edit_milestone(request, username, milestone_id=None):
    milestone = None
    if milestone_id:
        try:
            milestone = TaskModels.TaskMilestone.objects.get(pk=milestone_id)
        except TaskModels.TaskMilestone.DoesNotExist:
            pass
        else:
            if milestone.user.id != request.user.id:
                return HttpResponseRedirect(reverse('task:list_milestones', kwargs={"username": request.user.username}))

    form = TaskForms.TaskMilestoneForm(request.POST or None, instance=milestone)
    if form.is_valid():
        milestone = form.save(commit=False)
        if not form.instance.pk:
            # New instance, attach user
            milestone.user = request.user
        milestone.save()
        return HttpResponseRedirect(reverse('task:list_milestones', kwargs={"username": request.user.username}))
    return render(request, "task/changemilestone.html", {"form": form, "milestone": milestone})

@login_required
def add_triage_category(request, username):
    return edit_triage_category(request, None)

@login_required
def edit_triage_category(request, username, triage_category_id=None):
    triage = None
    if triage_category_id:
        try:
            triage = TaskModels.TaskTriageCategory.objects.get(pk=triage_category_id)
        except TaskModels.TaskTriageCategory.DoesNotExist:
            pass
        else:
            if triage.user.id != request.user.id:
                return HttpResponseRedirect(reverse('task:list_triage_category', kwargs={"username": request.user.username}))

    form = TaskForms.TaskTriageCategoryForm(request.POST or None, instance=triage)
    if form.is_valid():
        triage = form.save(commit=False)
        if not form.instance.pk:
            # New instance, attach user
            triage.user = request.user
        triage.save()
        return HttpResponseRedirect(reverse('task:list_triage_category', kwargs={"username": request.user.username}))
    return render(request, "task/changetriage.html", {"form": form, "triage": triage})

@login_required
def dashboard(request):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    deltadate = today + datetime.timedelta(days=7)

    task_week = TaskModels.Task.objects.filter(tasklist__user__id=request.user.pk,
                                                completed=False,
                                                due_date__range=[today, deltadate],
                                        ).order_by("-triage__priority")

    task_nodue = TaskModels.Task.objects.filter(tasklist__user__id=request.user.pk,
                                                completed=False,
                                                due_date=None
                                        ).order_by("-triage__priority")

    task_overdue = TaskModels.Task.objects.filter(tasklist__user__id=request.user.pk,
                                                completed=False,
                                                due_date__lte=today
                                        ).order_by("-triage__priority")

    return render(request, "task/dashboard.html", {"task_week": task_week,
                                                   "task_nodue": task_nodue,
                                                   "task_overdue": task_overdue})

@login_required
def calendar(request):
    calendar = TaskUtils.calendarize(request.user.pk, 30)
    return render(request, "task/calendar.html", {"calendar": calendar })

