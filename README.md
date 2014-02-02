#triage
A todo manager for the disaster that is your day.

##Build Status
[![Build Status](https://travis-ci.org/SamStudio8/triage.png)](https://travis-ci.org/SamStudio8/triage)
[![Coverage Status](https://coveralls.io/repos/SamStudio8/triage/badge.png?branch=master)](https://coveralls.io/r/SamStudio8/triage?branch=master)

## Technology Readiness Level
Consider this a pre-Alpha, work-in-progress; the Master branch should be in a stable condition.  
Expect the URLs, API and database schema to change, frequently, South migrations will be provided where appropriate.  
Changes which require further action are listed in CHANGELOG.
**Please don't use in prod!**

## Dependencies

    pip install Django south django-crispy-forms markdown

## Configuration

Copy triage/settings_example.py to triage/settings.py and fill in with the correct details such as database driver and static URLs.  
Copy triage/wsgi_example.py to triage/wsgi.py and add the path (this path may be unneccessary depending on your deployment).
    
    python manage.py syncdb
    python manage.py migrate task
    python manage.py migrate event
    python manage.py collectstatic

## Testing

To deploy the modest test suite on the `task` app;
    
    python manage.py test task

## Licence
Triage is licensed under the European Union Public Licence (EUPL v.1.1)  
See COPYING for further information.

