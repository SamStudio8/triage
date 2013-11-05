**Please don't use in prod**

### Dependancies

    pip install Django south

### Configuration

Copy settings_example.py to settings.py and fill in with the correct details such as database driver and static URLs.
    
    python manage.py syncdb
    python manage.py migrate task
    python manage.py collectstatic
