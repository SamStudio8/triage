#CHANGELOG

####0.0.90

Install django-crispy-forms and update static files for new CSS

    pip install django-crispy-forms
    python manage.py collectstatic

Add 'crispy_forms' to INSTALLED_APPS in your triage/settings.py
Add "CRISPY_TEMPLATE_PACK = 'bootstrap3'" to your triage/settings.py

####0.0.88

Allow null values for `EventFieldChange original`, `EventFieldChange.new`

    python mange.py migrate event

####0.0.75

Add 'event' to INSTALLED_APPS in your triage/settings.py

    python mange.py migrate event
