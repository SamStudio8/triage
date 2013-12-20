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

