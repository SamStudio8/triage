import datetime
from django.db.models import Count
from django.utils.timezone import utc

import task.models as TaskModels

_DEFAULT_TRIAGE = {
    "Urgent": {
        "name": "Urgent",
        "bg_colour": "000",
        "fg_colour": "ff0000",
        "priority": "100",
    },
    "Major": {
        "name": "Major",
        "bg_colour": "d9534f",
        "fg_colour": "fff",
        "priority": "10",
    },
    "Minor": {
        "name": "Minor",
        "bg_colour": "f0ad4e",
        "fg_colour": "fff",
        "priority": "5",
    },
    "Low": {
        "name": "Low",
        "bg_colour": "5cb85c",
        "fg_colour": "fff",
        "priority": "1",
    },
    "Very Low": {
        "name": "Very Low",
        "bg_colour": "428bca",
        "fg_colour": "fff",
        "priority": "0",
    },
    "Future": {
        "name": "Future",
        "bg_colour": "ccc",
        "fg_colour": "000",
        "priority": "-1",
    }
}

def create_default_triage_categories(uid):
    for TRIAGE in _DEFAULT_TRIAGE:
        _DEFAULT_TRIAGE[TRIAGE]["user_id"] = uid
        tcat = TaskModels.TaskTriageCategory.objects.create(**_DEFAULT_TRIAGE[TRIAGE])
        tcat.save()

def calendarize(uid, num_days, tasklist_id=0):
    today = datetime.date.today()
    deltadate = today + datetime.timedelta(days=num_days)

    tasks = TaskModels.Task.objects.filter(completed=False,
                                           due_date__range=[today, deltadate],
                                    ).order_by("triage__priority")
    milestones = []

    if uid:
        # Fetch all tasks on any lists owned by a particular user
        tasks = tasks.filter(tasklist__user__id=uid)
        milestones = TaskModels.TaskMilestone.objects.filter(user__id=uid,
                due_date__range=[today, deltadate])

    if tasklist_id:
        # Fetch all tasks on a particular list
        tasks = tasks.filter(tasklist=tasklist_id)

    calendar = {}
    for i, date in enumerate([today + datetime.timedelta(days=x) for x in range(num_days)]):
        calendar[i] = {}
        calendar[i]["month"] = date.strftime("%b")
        calendar[i]["day"] = date.day
        calendar[i]["datestamp"] = "%d %d" % (date.month, date.day)

        calendar[i]["tasks"] = []
        for task in filter(lambda t: t.due_date.date() == date, tasks):
            calendar[i]["tasks"].append(task)

        if uid:
            calendar[i]["milestones"] = []
            for milestone in filter(lambda t: t.due_date.date() == date, milestones):
                calendar[i]["milestones"].append(milestone)
    return calendar

def fetch_public_tasklists(uid):
    return TaskModels.TaskList.objects.filter(user__pk=uid, public=True)

def recently_added(uid, limit=5):
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid).order_by("creation_date")[:limit].reverse()

def recently_closed(uid, limit=5):
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=True).order_by("completed_date")[:limit].reverse()

def upcoming_tasks(uid, offset=0, days=7):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    offset_date = today + datetime.timedelta(days=offset)
    delta_date = today + datetime.timedelta(days=days+offset)

    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=False, due_date__range=[offset_date, delta_date]).order_by("-triage__priority", "due_date")

def overdue_tasks(uid):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=False, due_date__lte=today).order_by("-due_date")

def open_tasks(uid):
    return TaskModels.Task.objects.annotate(null=Count("due_date")).filter(tasklist__user__pk=uid, completed=False).order_by("-null", "due_date", "-triage__priority")

def closed_tasks(uid):
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=True).order_by("-completed_date")

def undue_tasks(uid):
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=False, due_date=None)

def untriage_tasks(uid):
    return TaskModels.Task.objects.filter(tasklist__user__pk=uid, completed=False, triage=None)
