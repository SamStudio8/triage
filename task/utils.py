import datetime
from django.utils.timezone import utc

import task.models as TaskModels

def create_default_triage_categories(uid):
    DEFAULT_TRIAGE = {
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

    for TRIAGE in DEFAULT_TRIAGE:
        DEFAULT_TRIAGE[TRIAGE]["user_id"] = uid
        tcat = TaskModels.TaskTriageCategory.objects.create(**DEFAULT_TRIAGE[TRIAGE])
        tcat.save()

def calendarize(uid, num_days, tasklist_id=0):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
    deltadate = today + datetime.timedelta(days=num_days)

    tasks = TaskModels.Task.objects.filter(tasklist__user__id=uid,
                                           completed=False,
                                           due_date__range=[today, deltadate],
                                    ).order_by("triage__priority")
    if tasklist_id:
        tasks = tasks.filter(tasklist=tasklist_id)

    calendar = {}
    for i, date in enumerate([today + datetime.timedelta(days=x) for x in range(num_days)]):
        calendar[i] = {}
        calendar[i]["month"] = date.strftime("%b")
        calendar[i]["day"] = date.day
        calendar[i]["datestamp"] = "%d %d" % (date.month, date.day)
        calendar[i]["tasks"] = []
        for task in sorted(filter(lambda t: t.due_date.day == date.day, tasks), key=lambda t: t.due_date):
            calendar[i]["tasks"].append(task)
    return calendar
