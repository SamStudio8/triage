import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc

import task.models as TaskModels
import task.forms as TaskForms
import task.events as TaskEvents
import event.utils as EventUtils

@login_required
def list_tasks(request):
    tasklists = request.user.tasklists.all()
    for tasklist in tasklists:
        tasklist.completed = tasklist.tasks.filter(completed=True).count()
        tasklist.uncompleted = tasklist.tasks.filter(completed=False).count()
    return render(request, "task/list.html", {"tasklists": tasklists})

@login_required
def add_task(request, tasklist_id=None):
    return edit_task(request, None, tasklist_id)

@login_required
def view_task(request, task_id=None):
    task = get_object_or_404(TaskModels.Task, pk=task_id)
    if task.tasklist.user.id != request.user.id:
        return HttpResponseRedirect(reverse('home'))
    history = EventUtils._get_history(task)
    return render(request, "task/view.html", {"task": task, "history": history})

@login_required
def edit_task(request, task_id, tasklist_id=None):

    if tasklist_id:
        tasklist = get_object_or_404(TaskModels.TaskList, pk=tasklist_id)
        if tasklist.user.id != request.user.id:
            return HttpResponseRedirect(reverse('home'))

    task = None
    if task_id:
        try:
            task = TaskModels.Task.objects.get(pk=task_id)
        except TaskModels.Task.DoesNotExist:
            pass
        else:
            if task.tasklist.user.id != request.user.id:
                return HttpResponseRedirect(reverse('home'))
            tasklist_id = task.tasklist_id

    form = TaskForms.TaskForm(request.user.id, request.POST or None,
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
def complete_task(request, task_id):
    task = get_object_or_404(TaskModels.Task, pk=task_id)
    if task.tasklist.user.id != request.user.id:
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
    if task.tasklist.user.id != request.user.id:
        return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskLinkForm(request.user.id, request.POST or None,
            initial={'from_task': task.pk})

    if form.is_valid():
        link = form.save()
        TaskEvents.LinkChange(request, link)
        return HttpResponseRedirect(reverse('task:view_task', args=(task.pk,)))
    return render(request, "task/changelink.html", {"form": form})

@login_required
def add_tasklist(request):
    return edit_tasklist(request)

@login_required
def edit_tasklist(request, tasklist_id=None):
    try:
        tasklist = TaskModels.TaskList.objects.get(pk=tasklist_id)
    except TaskModels.TaskList.DoesNotExist:
        tasklist = None
    else:
        if tasklist.user.id != request.user.id:
            return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskListForm(request.POST or None, instance=tasklist)
    if form.is_valid():
        tasklist = form.save(commit=False)
        if not form.instance.pk:
            # New list, attach user
            tasklist.user = request.user
        tasklist.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/changelist.html", {"form": form, "tasklist": tasklist})

@login_required
def list_triage_category(request):
    triages = request.user.triages.all()
    return render(request, "task/triages.html", {"triages": triages})

@login_required
def add_triage_category(request):
    return edit_triage_category(request, None)

@login_required
def edit_triage_category(request, triage_category_id=None):
    triage = None
    if triage_category_id:
        try:
            triage = TaskModels.TaskTriageCategory.objects.get(pk=triage_category_id)
        except TaskModels.TaskTriageCategory.DoesNotExist:
            pass
        else:
            if triage.user.id != request.user.id:
                return HttpResponseRedirect(reverse('task:list_triage_category'))

    form = TaskForms.TaskTriageCategoryForm(request.POST or None, instance=triage)
    if form.is_valid():
        triage = form.save(commit=False)
        if not form.instance.pk:
            # New instance, attach user
            triage.user = request.user
        triage.save()
        return HttpResponseRedirect(reverse('task:list_triage_category'))
    return render(request, "task/changetriage.html", {"form": form, "triage": triage})

@login_required
def dashboard(request):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    deltadate = today + datetime.timedelta(days=7)

    task_week = TaskModels.Task.objects.filter(tasklist__user__id=request.user.pk,
                                                completed=False,
                                                due_date__gte=today,
                                                due_date__lte=deltadate
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
