#CHANGELOG

####0.1.3-483D

TaskMilestones are now a property of a particular TaskList rather than a User  
**Migrating backwards can potentially leave a User with multiple copies of a milestone which will need to be pruned**

    python mange.py migrate task

####0.1.3-446D

Milestones displayed on calendar (dotted lines) and enumerated on dashboard  

    python manage.py collectstatic

####0.1.3-440D

Using `color` fields on milestone and triage settings forms  

####0.1.3-436D

Removed bootstrap-datetimepicker  

    python manage.py collectstatic

####0.1.3-431D

Allow tasks to actually be re-opened  
Improved dashboard now uses tabbed navigation  
Responsive calendar now uses touch scolling on smaller devices  
Fixed link_task causing HTTP500  

    python manage.py collectstatic

####0.1.3-406D

Introduce use of Django messages framework to deliver success status on Task quick_add  

####0.1.3-400D

Dropped `Task.progress`  

    python mange.py migrate task

####0.1.3-396D

Improved `view_tasklist`, now features upcoming (week and month) sublists and recently added and completed  

    python manage.py collectstatic

####0.1.3

Improved test coverage  
Remove /listslug/new-task/ URL and just use GET to /task/new/  
Users can now delete TaskLists (but are required to migrate all tasks contained to another list)  

####0.1.2

@danharibo strikes again with halfway upsidedown frown functionality  
Drop /list/ from URL scheme in favour of username/tasklist  
Move /triage/, /milestone/ to /settings/triage/, /settings/milestone/  
Show message for lists with no open tasks  
Catch empty attributes on `view_task`  
Following a POST users will typically be redirected to the previous page  
Added context_processor to return current url for use in post-POST redirection  
Update your triage/settings.py as demonstrated below  
Added fields to `Task`: `Task.created_by`, `Task.modified_by`  
Use `EventRecord` to determine creator and last modifier  
Removed recently added fields: `Task.created_by`, `Task.modified_by`  
Patch critical security issue that allowed editing models that had view permissions  

    python manage.py collectstatic

    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        "task.context_processors.current_url",
    )

####0.1.1

`TaskMilestone` model  
`TaskList` detail view  
Added glorious favicon, courtesy of @danharibo  
Improve interfaces on smaller devices  
Prevent users from assigning a task a milestone that they do not own!  
URL scheme updated  
Allow empty input for `Task.progress` (defaults to 0)  
Quick Task add form available in navigation bar  
If not creating, `edit_task` will autopopulate POST with missing values from model to allow partial form completion to not throw required field errors  
Overdue tasks can be rescheduled directly from the dashboard  
Hide completed tasks from the main list by default  
Removed requirement to be logged in to access view_task and view_tasklist  
Provide an option to share a tasklist and all tasks on that list publically  
Introduced user profiles to display public tasklists  


    python mange.py migrate task
    python manage.py collectstatic

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
