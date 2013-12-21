#CHANGELOG

####0.0.213D

Calendar CSS

    python manage.py collectstatic

####0.0.204D

Added `slug` field to `TaskList`, auto-populated using `slugify`

    python mange.py migrate task

####0.0.182D

Dashboard CSS

    python manage.py collectstatic

####0.0.166D

Replaced datetime picker

    python manage.py collectstatic

####0.0.142D

Render `Task` descriptions in Markdown, requires `python-markdown`  

    pip install markdown

####0.0.142D

Added `order` field to `TaskList`, allow longer `TaskList` names

    python mange.py migrate task

####0.0.131D

Add a user-centric `_id` field to `Task`, migrate to add and autopopulate new field

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
