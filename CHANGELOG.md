#CHANGELOG

####0.1.288D

Introduced user profiles to display public tasklists

####0.1.274D

Provide an option to share a tasklist and all tasks on that list publically  
Removed requirement to be logged in to access view_task and view_tasklist  

    python mange.py migrate task

####0.1.273D

Hide completed tasks from the main list by default  

####0.1.271D

Overdue tasks can be rescheduled directly from the dashboard  
If not creating, `edit_task` will autopopulate POST with missing values from model to allow partial form completion to not throw required field errors

####0.1.265D

Quick Task add form available in navigation bar  
Allow empty input for `Task.progress` (defaults to 0)

    python manage.py collectstatic

####0.1.257D

URL scheme updated

####0.1.238D

Prevent users from assigning a task a milestone that they do not own!

####0.1.237D

Improve interfaces on smaller devices  
Added glorious favicon, courtesy of @danharibo  
`TaskList` detail view  
`TaskMilestone` model

    python manage.py collectstatic
    python mange.py migrate task

####0.1.0

Add a user-centric `_id` field to `Task`, migrate to add and autopopulate new field  
Added `order` field to `TaskList`, allow longer `TaskList` names  
Render `Task` descriptions in Markdown, requires `python-markdown`  
Replaced datetime picker  
Added `slug` field to `TaskList`, auto-populated using `slugify`  
Dashboard and Calendar

    pip install markdown
    python manage.py collectstatic
    python mange.py migrate task

####0.0.128

Templates for the `account` app are now found at `account/templates`  

####0.0.128

Update CSS

    python manage.py collectstatic

####0.0.127

New login view design and sticky footer

    python manage.py collectstatic

####0.0.120

Travis and Coveralls support

####0.0.109

EventLinkChange

    python mange.py migrate event

####0.0.103

Enforce unique pair (`from_task`, `to_task`) in `TaskLink` model

    python mange.py migrate task

####0.0.102

`TaskLink` models

    python mange.py migrate task

####0.0.98

Removed `Task.parent`

    python mange.py migrate task

####0.0.94

Update static files for new CSS

    python manage.py collectstatic

####0.0.90

Install django-crispy-forms and update static files for new CSS

    pip install django-crispy-forms
    python manage.py collectstatic

Add `'crispy_forms'` to INSTALLED_APPS in your triage/settings.py  
Add `CRISPY_TEMPLATE_PACK = 'bootstrap3'` to your triage/settings.py

####0.0.88

Allow null values for `EventFieldChange original`, `EventFieldChange.new`

    python mange.py migrate event

####0.0.75

Add 'event' to INSTALLED_APPS in your triage/settings.py

    python mange.py migrate event
