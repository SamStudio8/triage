#triage
A todo manager for the disaster that is your day.

## Technology Readiness Level
Consider this a pre-Alpha, work-in-progress; the Master branch should be in a stable condition.  
Expect the URLs, API and database schema to change, frequently, South migrations will be provided where appropriate.  
**Please don't use in prod!**

## Dependencies

    pip install Django south

## Configuration

Copy triage/settings_example.py to triage/settings.py and fill in with the correct details such as database driver and static URLs.
    
    python manage.py syncdb
    python manage.py migrate task
    python manage.py collectstatic

## Testing

To deploy the modest test suite on the `task` app;
    
    python manage.py test task

## Licence
Triage is licensed under the European Union Public Licence (EUPL v.1.1)  
See COPYING for further information.

