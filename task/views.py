from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import task.models as TaskModels
import task.forms as TaskForms

def list_tasks(request):
    return render(request, "task/list.html")

@login_required
def add_tasklist(request, tasklist_id=0):
    # Permissions
    try:
        tasklist = TaskModels.TaskList.objects.get(pk=tasklist_id)
    except TaskModels.TaskList.DoesNotExist:
        tasklist = None

    form = TaskForms.TaskListForm(request.POST or None, instance=tasklist)
    if form.is_valid():
        tasklist = form.save(commit=False)
        tasklist.user = request.user
        tasklist.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/changelist.html", {"form": form, "tasklist": tasklist})

@login_required
def add_task(request, tasklist_id):
    # Permissions
    tasklist = get_object_or_404(TaskModels.TaskList, pk=tasklist_id)
    return edit_task(request, 0, tasklist_id)

@login_required
def edit_task(request, task_id, tasklist_id=0):
    # Permissions
    try:
        task = TaskModels.Task.objects.get(pk=task_id)
    except TaskModels.Task.DoesNotExist:
        task = None

    form = TaskForms.TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save(commit=False)
        task.tasklist_id = tasklist_id #What if 0?
        task.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/changetask.html", {"form": form, "task": task})
