import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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
def new_task(request, username):
    listslug = request.GET.get("tasklist", None)
    if listslug:
        tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
        if tasklist.has_edit_permission(request.user.pk):
            return edit_task(request, username, None, tasklist.pk)
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return edit_task(request, username, None, None)

def view_tasklist(request, username, listslug):
    tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
    if not tasklist.has_view_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))
    calendar = TaskUtils.calendarize(None, 30, tasklist.pk)
    edit_permission = tasklist.has_edit_permission(request.user.pk)
    return render(request, "task/tasklist.html", {"tasklist": tasklist,
                                                  "calendar": calendar,
                                                  "recently_added": tasklist.recently_added(limit=5),
                                                  "recently_closed": tasklist.recently_closed(limit=5),
                                                  "upcoming_week": tasklist.upcoming_tasks(days=7),
                                                  "upcoming_month": tasklist.upcoming_tasks(offset=7, days=30),
                                                  "overdue": tasklist.overdue_tasks,
                                                  "edit_permission": edit_permission})

def view_task(request, username, task_id):
    task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
    if not task.has_view_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))
    history = EventUtils._get_history(task)
    edit_permission = task.has_edit_permission(request.user.pk)
    return render(request, "task/view.html", {"task": task,
                                              "history": history,
                                              "edit_permission": edit_permission})

def view_milestone(request, username, listslug, milestone_id):
    milestone = get_object_or_404(TaskModels.TaskMilestone, tasklist__user__username=username, pk=milestone_id)
    edit_permission = milestone.has_edit_permission(request.user.pk)

    if not milestone.has_view_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))
    return render(request, "task/milestone.html", {"milestone": milestone,
                                                  "edit_permission": edit_permission})


@login_required
def edit_task(request, username, task_id, tasklist_id=None):

    if tasklist_id:
        tasklist = get_object_or_404(TaskModels.TaskList, pk=tasklist_id)
        if not tasklist.has_edit_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))

    milestone_id = None
    milestone = request.GET.get("milestone", None)
    if milestone:
        milestone = get_object_or_404(TaskModels.TaskMilestone, tasklist__user__username=username, pk=milestone)
        if not milestone.has_edit_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))
        milestone_id = milestone.pk

    task = None
    if task_id:
        task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
        if not task.has_edit_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))
        tasklist_id = task.tasklist_id

        if task.milestone:
            milestone_id = task.milestone.pk


    form = TaskForms.TaskForm(
               request.user.id,
               tasklist_id,
               request.POST.get('form_type', None),
               request.POST or None,
               initial={
                   'tasklist': tasklist_id,
                   'milestone': milestone_id
               },
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

        # Save the history, make a CreationEvent if Task is new
        if not original:
            TaskEvents.CreationEvent(request, task)
        TaskEvents.FieldChange(request, original, task)

        # Display a message if this was sent from quick_add
        if request.POST.get('quick', None):
            url = reverse('task:view_task', kwargs={"username": task.tasklist.user.username,
                                                    "task_id": task.local_id})
            msg = "Task <b><a class='alert-link' href='" + url + "'>#" + str(task.local_id) + ": " + task.name + "</a></b> added successfully."
            messages.add_message(request, messages.SUCCESS, msg, extra_tags='safe')

        redirect_to = request.POST.get('next', "/")
        return HttpResponseRedirect(redirect_to)

    redirect_to = request.GET.get('next', "/")
    return render(request, "task/changetask.html", {"form": form,
                                                    "task": task,
                                                    "next": redirect_to})

@login_required
def complete_task(request, username, task_id):
    task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
    if not task.has_edit_permission(request.user.pk):
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

    redirect_to = request.GET.get('next', "/")
    return HttpResponseRedirect(redirect_to)

@login_required
def link_task(request, username, task_id):
    task = get_object_or_404(TaskModels.Task, tasklist__user__username=username, _id=task_id)
    if not task.has_edit_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskLinkForm(request.user.id, request.POST or None,
            initial={'from_task': task.pk})

    if form.is_valid():
        link = form.save()
        TaskEvents.LinkChange(request, link)
        return HttpResponseRedirect(reverse('task:view_task', kwargs={"username": task.tasklist.user.username,
                                                                      "task_id": task.local_id}))
    return render(request, "task/changelink.html", {"form": form})

@login_required
def add_tasklist(request, username):
    return edit_tasklist(request, username)

@login_required
def edit_tasklist(request, username=None, listslug=None):
    tasklist = None
    if username and listslug:
        tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
        if not tasklist.has_edit_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskListForm(request.user.id, request.POST or None, instance=tasklist)
    if form.is_valid():
        tasklist = form.save(commit=False)

        # Update the redirect (if needed) if the slug will be changed!
        redirect_to = request.POST.get('next', "/")
        if tasklist.id and tasklist.slug != slugify(form.cleaned_data["name"]):
            if tasklist.slug in redirect_to:
                redirect_to = redirect_to.replace(tasklist.slug, slugify(form.cleaned_data["name"]))

        if not form.instance.pk:
            # New list, attach user
            tasklist.user = request.user
            tasklist.slug = slugify(form.cleaned_data["name"])
        tasklist.save()

        return HttpResponseRedirect(redirect_to)

    redirect_to = request.GET.get('next', "/")
    return render(request, "task/changelist.html", {"form": form,
                                                    "tasklist": tasklist,
                                                    "next": redirect_to})

@login_required
def delete_tasklist(request, username=None, listslug=None):
    tasklist = None
    if username and listslug:
        tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
        if not tasklist.has_edit_permission(request.user.pk):
            return HttpResponseRedirect(reverse('home'))

    form = TaskForms.TaskListDeleteForm(request.user.id, tasklist.pk, request.POST or None)
    if form.is_valid():
        transfer_to = form.cleaned_data["tasklist_transfer"]

        # Transfer Tasks and Delete
        # TODO Currently assuming user has right to move all tasks in a list
        # NOTE This is a fair assumption given the current permission model
        for task in TaskModels.Task.objects.filter(tasklist__pk=tasklist.pk):
            task.tasklist = transfer_to
            task.save()
        tasklist.delete()

        # Update the redirect to the list that tasks will be transferred to
        redirect_to = request.POST.get('next', "/")
        redirect_to = redirect_to.replace(tasklist.slug, transfer_to.slug)
        return HttpResponseRedirect(redirect_to)

    redirect_to = request.GET.get('next', "/")
    return render(request, "task/deletelist.html", {"form": form,
                                                    "tasklist": tasklist,
                                                    "next": redirect_to})

@login_required
def list_triage_category(request, username):
    triages = request.user.triages.all()
    return render(request, "task/triages.html", {"triages": triages})

@login_required
def list_milestones(request, username, listslug):
    tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
    if not tasklist.has_edit_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))

    return render(request, "task/milestones.html", {"tasklist": tasklist})

@login_required
def new_milestone(request, username, listslug):
    tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
    if not tasklist.has_edit_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))

    return edit_milestone(request, username, tasklist.slug, milestone_id=None)

@login_required
def edit_milestone(request, username, listslug, milestone_id=None):
    milestone = None

    tasklist = get_object_or_404(TaskModels.TaskList, slug=listslug, user__username=username)
    if not tasklist.has_edit_permission(request.user.pk):
        return HttpResponseRedirect(reverse('home'))

    if milestone_id:
        try:
            milestone = TaskModels.TaskMilestone.objects.get(pk=milestone_id)
        except TaskModels.TaskMilestone.DoesNotExist:
            pass
        else:
            if milestone.tasklist.user.id != request.user.id:
                return HttpResponseRedirect(reverse('task:list_milestones',
                                            kwargs={
                                                "username": request.user.username,
                                                "listslug": milestone.tasklist.slug
                                            }))

    form = TaskForms.TaskMilestoneForm(request.POST or None, instance=milestone)
    if form.is_valid():
        milestone = form.save(commit=False)
        if not form.instance.pk:
            # New instance, attach tasklist
            milestone.tasklist = tasklist
        milestone.save()

        redirect_to = request.POST.get('next', reverse('task:list_milestones',
                                                  kwargs={
                                                    "username": request.user.username,
                                                    "listslug": tasklist.slug
                                                  })
        )
        return HttpResponseRedirect(redirect_to)

    redirect_to = request.GET.get('next', reverse('task:list_milestones',
                                              kwargs={
                                                "username": request.user.username,
                                                "listslug": tasklist.slug
                                              })
    )
    return render(request, "task/changemilestone.html", {"form": form,
                                                    "milestone": milestone,
                                                    "next": redirect_to})

@login_required
def add_triage_category(request, username):
    return edit_triage_category(request, None)

@login_required
def edit_triage_category(request, username, triage_category_id=None):
    triage = None
    if triage_category_id:
        triage = get_object_or_404(TaskModels.TaskTriageCategory, pk=triage_category_id)
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
    calendar = TaskUtils.calendarize(request.user.pk, 30)
    return render(request, "task/dashboard.html", {
        "calendar": calendar,
        "oc_cal": TaskUtils.calendarize_open_closed(request.user.pk, 5),
        "milestones": TaskUtils.upcoming_milestones(request.user.pk, offset=0, days=0),
        "recently_added": TaskUtils.recently_added(request.user.pk, limit=10),
        "recently_closed": TaskUtils.recently_closed(request.user.pk, limit=10),
        "upcoming_week": TaskUtils.upcoming_tasks(request.user.pk, days=7),
        "upcoming_month": TaskUtils.upcoming_tasks(request.user.pk, offset=7, days=23),
        "overdue": TaskUtils.overdue_tasks(request.user.pk),
        "no_due": TaskUtils.undue_tasks(request.user.pk),
        "no_triage": TaskUtils.untriage_tasks(request.user.pk),
        "open_tasks": TaskUtils.open_tasks(request.user.pk),
        "closed_tasks": TaskUtils.closed_tasks(request.user.pk),
        "edit_permission": True, # NOTE Currently a user has edit permission for any task on their dashboard
        "dashboard": True
    })

@login_required
def housekeeping(request):
    return render(request, "task/housekeeping.html", {
        "no_due": TaskUtils.undue_tasks(request.user.pk),
        "no_triage": TaskUtils.untriage_tasks(request.user.pk),
        "edit_permission": True, # NOTE Currently a user has edit permission for any task on their dashboard
    })

@login_required
def calendar(request):
    calendar = TaskUtils.calendarize(request.user.pk, 30)
    return render(request, "task/calendar.html", {"calendar": calendar })

def profile(request, username):
    user = get_object_or_404(User, username=username)
    tasklists = TaskUtils.fetch_public_tasklists(user.pk)
    return render(request, "task/profile.html", {"profile": user,
                                                 "tasklists": tasklists})
